# -*- coding: utf-8 -*-
{
    "name": "AnaConEx Solutions - Purchase Excel Reports",
    "version": '13.1.0.0',
    'license': 'AGPL-3',
    "category": 'Purchase',
    "summary": """
        Custom Purchase Report
        """,
    "description": """
        - Custom Purchase Report
    """,
    "sequence": 1,
    "author": "AnaConEx Solutions LLC",
    "website": "https://www.anaconex.com/",
    "depends": ['purchase', 'report_xlsx', 'product'],
    "data": [
        # 'data/fields_adder.xml',
        'security/ir.model.access.csv',
        'views/menu_report_xls.xml',
        'wizard/purchase_order_report_wizard.xml',
    ],
    
    "price": 0,
    "currency": 'USD',
    "installable": True,
    "application": True,
    "auto_install": False,
}