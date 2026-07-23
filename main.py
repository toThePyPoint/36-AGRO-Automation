from pathlib import Path
from datetime import date

import numpy as np
import pandas as pd

from maps import mblb_dtypes, mblb_columns_names, zkbe1_dtypes, zkbe1_columns_names, buffer_roundings_dtypes


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


RECEPIENTS = "magdalena.mardon@rotofrank.com; kamil.daniewski@rotofrank.com"


source_files_dir = Path(r"P:/Technisch/PLANY PRODUKCJI/PLANIŚCI/PP_TOOLS_TEMP_FILES/17_AGRO/source_files")
helper_files_dir = Path(r"P:/Technisch/PLANY PRODUKCJI/PLANIŚCI/PP_TOOLS_TEMP_FILES/17_AGRO/helper_files")
output_files_dir = Path(r"P:/Technisch/PLANY PRODUKCJI/PLANIŚCI/PP_TOOLS_TEMP_FILES/17_AGRO/output_files")


# 1. Define filenames in ONE place using a dictionary
source_file_names = {
    "zkbe1_next_day": "zkbe1_next_day.XLSX",
    "zkbe1_today": "zkbe1_today.XLSX",
    "mblb": "mblb.XLSX"
}

helper_file_names = {
    "buffer_roundings": "buffer_roundings.xlsx",
}

output_file_names = {
    "final_df": "final_table.xlsx",
    "to_trigger_df": "to_trigger_table.xlsx",
}

# 2. Build full paths dynamically using a dictionary comprehension
source_files = {key: source_files_dir / name for key, name in source_file_names.items()}
helper_files = {key: helper_files_dir / name for key, name in helper_file_names.items()}
output_files = {key: output_files_dir / name for key, name in output_file_names.items()}


def generate_boxes_report():
    # 3. Check them all by passing the dictionary values
    if all(is_file_from_today(path) for path in source_files.values()):
        print("🚀 All files are fresh. Proceeding!")

        mblb_df = pd.read_excel(source_files["mblb"], dtype=mblb_dtypes)
        mblb_df = mblb_df.rename(columns=mblb_columns_names)
        mblb_df = mblb_df[['material_number', 'Agro_stock']]

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

        merged = merged.merge(mblb_df, on='material_number', how='left')

        merged = merged.assign(
            gap=0,
            to_trigger=0,
            quantity_after_issue=0
        )

        merged = merged[
            ['material_number', 'material_short_text', 'supplier_number', 'supplier_name', 'stock', 'safety_stock',
             'planned_delivery_time', 'buffer', 'firmed_issues_today', 'firmed_issues_next_day', 'gap', 'rounding',
             'to_trigger', 'Agro_stock', 'quantity_after_issue']]

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
        to_trigger_df.to_excel(output_files['to_trigger_df'], index=False)

    else:
        print("⚠️ Warning: One or more files are missing or out of date.")


if __name__ == "__main__":
    generate_boxes_report()