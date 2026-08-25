from pathlib import Path
from datetime import date, datetime

import numpy as np
import pandas as pd

from maps import (mblb_dtypes, mblb_columns_names, zkbe1_dtypes, zkbe1_columns_names, buffer_roundings_dtypes,
                  mb52_column_names, mb52_dtypes, zkbe1_de_columns_names, zkbe1_de_dtypes)

from send_email import send_email_from_application


zkbe1_columns_names = zkbe1_de_columns_names.copy()
zkbe1_dtypes = zkbe1_de_dtypes.copy()

def get_zkbe1_df(file_path, df_dtypes, df_columns_names):
    df = pd.read_excel(file_path, dtype=df_dtypes)
    df = df.rename(columns=df_columns_names)
    df['material_number'] = df['material_number'].astype(str)

    # Sort by material_number and stock (ascending order pushes 0 to the top)
    df = df.sort_values(by=['material_number', 'stock'], ascending=True)
    # Drop duplicates on material_number, keeping the LAST row (which will have the higher stock)
    df = df.drop_duplicates(subset=['material_number'], keep='last')

    return df

# Helper function
def is_file_from_today(file_path):
    if not file_path.exists():
        return False
    return date.fromtimestamp(file_path.stat().st_mtime) == date.today()


RECIPIENTS = "sekretariat@agrolubartow.pl"
CC_RECIPIENTS = "jaroslaw.keller@rotofrank.com; agrolubartow@o2.pl; jakub.sternik@rotofrank.com"


# source_files_dir = Path(r"P:/Technisch/PLANY PRODUKCJI/PLANIŚCI/PP_TOOLS_TEMP_FILES/17_AGRO/source_files")
source_files_dir = Path(r"\\rfmesrv5\connect\DST_SAP_Transfer\P11\PPS_LUB\06_AGRO")
# helper_files_dir = Path(r"P:/Technisch/PLANY PRODUKCJI/PLANIŚCI/PP_TOOLS_TEMP_FILES/17_AGRO/helper_files")
helper_files_dir = Path(r"P:\Zakupy\O\AGRO_Automation\helper_files")
# output_files_dir = Path(r"P:/Technisch/PLANY PRODUKCJI/PLANIŚCI/PP_TOOLS_TEMP_FILES/17_AGRO/output_files")
output_files_dir = Path(r"P:\Zakupy\O\AGRO_Automation\output_files")


# 1. Define filenames in ONE place using a dictionary
source_file_names = {
    # "zkbe1_next_day": "zkbe1_next_day.XLSX",
    # "zkbe1_today": "zkbe1_today.XLSX",
    # "mblb": "mblb.XLSX",
    "mb52": "PUR_LUB_004.xlsx",
    "zkbe1_next_day": "PUR_LUB_005.xlsx",
    "zkbe1_today": "PUR_LUB_006.xlsx",
}

helper_file_names = {
    "buffer_roundings": "buffer_roundings.xlsx",
}

output_file_names = {
    "final_df": "final_table.xlsx",
    "to_trigger_df": "kartony_wywolanie.xlsx",
    "to_trigger_html": "to_trigger.html",
}

# 2. Build full paths dynamically using a dictionary comprehension
source_files = {key: source_files_dir / name for key, name in source_file_names.items()}
helper_files = {key: helper_files_dir / name for key, name in helper_file_names.items()}
output_files = {key: output_files_dir / name for key, name in output_file_names.items()}


def generate_boxes_report():
    # 3. Check them all by passing the dictionary values
    if all(is_file_from_today(path) for path in source_files.values()):
        print("🚀 All files are fresh. Proceeding!")

        # mblb_df = pd.read_excel(source_files["mblb"], dtype=mblb_dtypes)
        # mblb_df = mblb_df.rename(columns=mblb_columns_names)
        # mblb_df = mblb_df[['material_number', 'Agro_stock']]

        mb52_df = pd.read_excel(source_files["mb52"], dtype=mb52_dtypes)
        mb52_df = mb52_df.rename(columns=mb52_column_names)
        mb52_df = mb52_df[mb52_df['special_stock_number'] == '640912']
        mb52_df = mb52_df[['material_number', 'Agro_stock']]

        zkbe1_next_day_df = get_zkbe1_df(file_path=source_files['zkbe1_next_day'], df_dtypes=zkbe1_dtypes,
                                         df_columns_names=zkbe1_columns_names)
        zkbe1_next_day_df = zkbe1_next_day_df[
            ['material_number', 'material_short_text', 'supplier_number', 'supplier_name', 'stock', 'safety_stock',
             'planned_delivery_time', 'firmed_issues']]

        zkbe1_today_df = get_zkbe1_df(file_path=source_files['zkbe1_today'], df_dtypes=zkbe1_dtypes,
                                      df_columns_names=zkbe1_columns_names)
        zkbe1_today_df = zkbe1_today_df[['material_number', 'firmed_issues']]

        zkbe1_merged = zkbe1_next_day_df.merge(zkbe1_today_df, on='material_number', how='left',
                                               suffixes=('_next_day', '_today'))

        buffer_roundings_df = pd.read_excel(helper_files["buffer_roundings"], dtype=buffer_roundings_dtypes)
        buffer_roundings_df = buffer_roundings_df.drop(columns=['mat_description'])

        merged = zkbe1_merged.merge(buffer_roundings_df, on='material_number', how='left')

        merged = merged.merge(mb52_df, on='material_number', how='left')

        merged = merged.assign(
            gap=0,
            to_trigger=0,
            quantity_after_issue=0
        )

        merged['Agro_stock'] = merged['Agro_stock'].fillna(0)

        merged = merged[
            ['material_number', 'material_short_text', 'supplier_number', 'supplier_name', 'stock', 'safety_stock',
             'planned_delivery_time', 'buffer', 'firmed_issues_today', 'firmed_issues_next_day', 'gap', 'rounding',
             'to_trigger', 'Agro_stock', 'quantity_after_issue', 'comment']]

        # --- Formulas ---
        # Column: GAP
        # --- 1. Logic for POSITIVE buffer (buffer > 0) ---
        diff = merged['stock'] - merged['buffer'] - merged['firmed_issues_next_day']
        positive_buffer_logic = np.where(diff >= 0, 0, diff * -1)

        # --- 2. Logic for OTHERWISE (buffer <= 0 or empty) ---
        # As established before, this Excel formula simplifies directly to the difference
        otherwise_logic = merged['firmed_issues_next_day'] - merged['firmed_issues_today']

        # --- 3. Combine using np.where ---
        merged['gap'] = np.where(
            merged['buffer'] > 0,
            positive_buffer_logic,
            otherwise_logic
        )

        # Column: TO_TRIGGER
        # If gap is greater than 0, take the maximum of gap and rounding. Otherwise, it's 0.
        merged['to_trigger'] = np.where(
            merged['gap'] > 0,
            np.maximum(merged['gap'], merged['rounding']),
            0
        )

        # Column: QUANTITY_AFTER_ISSUE
        positive_buffer_logic = merged['Agro_stock'] - merged['to_trigger']
        otherwise_logic = merged['stock'] - merged['firmed_issues_next_day']

        merged['quantity_after_issue'] = np.where(
            merged['buffer'] > 0,
            positive_buffer_logic,
            otherwise_logic
        )
        # --- Formulas ---

        merged.to_excel(output_files['final_df'], index=False)
        to_trigger_df = merged[merged['to_trigger'] > 0]

        to_trigger_df = to_trigger_df[['material_number', 'material_short_text', 'to_trigger', 'quantity_after_issue',
                                       'comment']]
        to_trigger_df = to_trigger_df.sort_values(by=['to_trigger'], ascending=[False])

        to_trigger_df = to_trigger_df.rename(
            columns={'material_number': 'Numer SAP', 'material_short_text': 'Nazwa', 'to_trigger': 'Ilość',
                     'comment': 'komentarz', 'quantity_after_issue': 'Ilość po wydaniu'})

        # to_trigger_df.to_excel(output_files['to_trigger_df'], index=False)

        # 1. Save the DataFrame using ExcelWriter and openpyxl engine
        with pd.ExcelWriter(
                output_files['to_trigger_df'], engine='openpyxl'
        ) as writer:
            to_trigger_df.to_excel(writer, index=False, sheet_name='Sheet1')

            # 2. Get the worksheet for modification
            worksheet = writer.sheets['Sheet1']

            # 3. Iterate through columns and adjust width
            for col in worksheet.columns:
                # Find the maximum string length in the current column
                max_len = max(len(str(cell.value or '')) for cell in col)
                # Get the column letter (e.g., 'A', 'B')
                col_letter = col[0].column_letter
                # Add padding (e.g., +3) so the text doesn't touch the edges
                worksheet.column_dimensions[col_letter].width = max(max_len + 3, 10)

        to_trigger_df.to_html(output_files['to_trigger_html'])

        # Send email
        # Load the HTML content
        # with open(output_files['to_trigger_html'], "r", encoding='utf-8') as file:
        #     html_content = file.read()

        date_today = datetime.today().strftime('%Y-%m-%d')

        email_body = f"""Dzień dobry, <br>
        
                      Kartony do wywołania.\n"""
        subject = f"Zamówienie kartonów AGRO z dn. {date_today}"
        send_email_from_application(RECIPIENTS, subject, email_body, output_files['to_trigger_df'], "PLIK",
                                    "", CC_RECIPIENTS)

    else:
        print("⚠️ Warning: One or more files are missing or out of date.")


if __name__ == "__main__":
    generate_boxes_report()