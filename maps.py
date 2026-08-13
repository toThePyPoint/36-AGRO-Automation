mblb_columns_names = {
    "Dostawca": "supplier",
    "Nazwisko (nazwa) 1": "name",
    "Materiał": "material_number",
    "Opis materiału": "material_description",
    "Nieogranicz.wykorz.": "Agro_stock",
    "Podst. jedn. miary": "base_unit_of_measure",
    "Wartość całkowita": "total_value"
}

mblb_dtypes = {
    "Dostawca": "string",
    "Materiał": "string",
}

mb52_column_names = {
    "Material": "material_number",
    "Bezeichnung": "material_description",
    "Frei verwendbar": "Agro_stock",  # Odpowiednik "Nieogranicz.wykorz."
    "Lagerort": "storage_location",
    "Basis-ME": "base_unit_of_measure",  # Odpowiednik "Podst. jedn. miary"
    "Gesperrt": "blocked_stock",
    "In QualPrüfung": "quality_inspection_stock",
    "Wert Sperrbestand": "blocked_stock_value",
    "SobNummer": "special_stock_number",  # Skrót od Sonderbestand Nummer
}

mb52_dtypes = {
    "Material": "string",
    "Lagerort": "string",
    "SobNummer": "string",
}

zkbe1_columns_names = {
    "Pio.ogólny": "general_priority",
    "Prio.zapasów": "stock_priority",
    "Best": "purchase_order",
    "NrMat.": "material_number",
    "Krótki tekst mater.": "material_short_text",
    "Minim. wielk. partii": "minimum_lot_size",
    "SzukCiągZna (IR)": "supplier_name",
    "Aktualny dostawca (IR)": "supplier_number",
    "Status RC": "rc_status",
    "Grupa zaopatrzeniowa": "purchasing_group",
    "WS": "valuation_type",
    "Kalendarz planowania": "planning_calendar",
    "MRP Kontr": "mrp_controller",
    "Wart.zaokrąg.": "rounding_value",
    "GP": "business_partner",
    "BP": "purchasing_block",
    "Zapas": "stock",
    "Zapas bezpieczeńst": "safety_stock",
    "Pewne wejścia": "firmed_receipts",
    "Ustalone wyjścia": "firmed_issues",
    "PlaCzasDos(IR)": "planned_delivery_time"
}

zkbe1_dtypes = {
    "Aktualny dostawca (IR)": "string",
    "Grupa zaopatrzeniowa": "string",
}

zkbe1_de_columns_names = {
    "GesamtPrio": "general_priority",
    "BestandsPrio": "stock_priority",
    "Best": "purchase_order",
    "MatNr.": "material_number",
    "Materialkurztext   :": "material_short_text",
    "Mind.LosGr.": "minimum_lot_size",
    "Suchbegriff (EIS)": "supplier_name",
    "Aktueller Lieferant (EIS)": "supplier_number",
    "Status RK": "rc_status",
    "Eink.Gruppe": "purchasing_group",
    "WSM": "valuation_type",
    "Planungskalender": "planning_calendar",
    "Disponent": "mrp_controller",
    "Rundg.Mg": "rounding_value",
    "GP": "business_partner",
    "BP": "purchasing_block",
    "Lagerbestand": "stock",
    "Sicherheitsbestand": "safety_stock",
    "Fester Zugang": "firmed_receipts",
    "Feste Abg. bis": "firmed_issues",
    "PLIFZ (EIS)": "planned_delivery_time"
}

zkbe1_de_dtypes = {
    "Aktueller Lieferant (EIS)": "string",
    "Eink.Gruppe": "string"
}

buffer_roundings_dtypes = {
    "material_number": "string",
}