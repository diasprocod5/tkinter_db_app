from tkinter import *
from tkinter import messagebox
table_data = {
            "clients": {
                "query": "SELECT client_id, full_name, phone, client_type, created_at, company_info "
                         "FROM clients ",
                "columns": ("id", "Name", "Phone","Is company", "Created","Company info"),
                "display_columns": ("Name", "Phone", "Is company",  "Created", "Company info",),  # Без id
                "column_widths": {"Name": 150, "Phone": 150, "Is company": 150,   "Created": 150, "Company info":330,},
                "rows": None
            },
            "tariffs": {
                "query": "SELECT * FROM tariffs",
                "columns": ("id", "Name", "Price", "Type", "Description"),
                "display_columns": ("Name", "Price", "Type", "Description"),  # Без id
                "column_widths": {"Name": 150, "Price": 150, "Type": 150, "Description": 800},
                "rows": None
            },
            "debtors": {
                "query": "SELECT * FROM get_debtors()",
                "columns": ("id", "Name","Phone","Balance","Debt", "Total debt"),
                "display_columns": ( "Name","Phone","Balance","Debt", "Total debt"),  # Без id
                "column_widths": { "Name":150,"Phone":150, "Balance":100,"Debt":100, "Total debt":100},
                "rows": None
            },
            "transactions": {
                "query": "SELECT * FROM transactions;",
                "columns": ("id", "Name", "Type", "Amount", "Date","Description"),
                "display_columns": ( "Name", "Type", "Amount", "Date","Description"),  # Без id
                "column_widths": {"Name":150, "Type":100, "Amount":100, "Date":150,"Description":450},
                "rows": None
            }
        }
