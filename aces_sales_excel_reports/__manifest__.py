{
    "name": "AnaConEx Solutions - Sales Excel Reports",
    "version": '13.1.0.0',
    'license': 'AGPL-3',
    "category": 'Sale',
    "summary": """
        Order Profitability and Sales Report
        """,
    "description": """
        - Order Profitability and Sales Report
    """,
    "sequence": 1,
    "author": "AnaConEx Solutions LLC",
    "website": "https://www.anaconex.com/",

    "depends": ['sale', 'report_xlsx', 'product'],
    "data": [
        'data/fields_adder.xml',
        'security/ir.model.access.csv',
        'views/menu_report_xls.xml',
        'wizard/order_profitability_report_wizard.xml',
        'wizard/sale_order_report_wizard.xml',
    ],
    "price": 0,
    "currency": 'USD',
    "installable": True,
    "application": True,
    "auto_install": False,
}