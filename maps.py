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

buffer_roundings_dtypes = {
    "material_number": "string",
}