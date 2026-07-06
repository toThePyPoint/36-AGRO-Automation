mblb_columns_names = {
    "Dostawca": "supplier",
    "Nazwisko (nazwa) 1": "name_1",
    "Materiał": "material",
    "Opis materiału": "material_description",
    "Nieogranicz. wykorz.": "unrestricted_use",
    "Podst. jedn. miary": "base_unit_of_measure",
    "Wartość całkowita": "total_value"
}

mblb_dtypes = {
    "Dostawca": "string",
    "Materiał": "string",
}

zkbe1_columns_names = {
    "Pio.ogólny": "general_priority",
    "Prio.zapasów": "stock_priority",
    "Best": "purchase_order",
    "NrMat.": "material_number",
    "Krótki tekst mater.": "material_short_text",
    "Minim. wielk. partii": "minimum_lot_size",
    "SzukCiągZna (IR)": "search_string_ir",
    "Aktualny dostawca (IR)": "current_supplier_ir",
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
    "PlaCzasDos(IR)": "planned_delivery_time_ir"
}

zkbe1_dtypes = {
    "Aktualny dostawca (IR)": "string",
    "Grupa zaopatrzeniowa": "string",
}