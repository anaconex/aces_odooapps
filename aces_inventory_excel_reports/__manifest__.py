# -*- coding: utf-8 -*-
{
    "name": "AnaConEx Solutions - Inventory Excel Reports",
    "version": '13.1.0.0',
    'license': 'AGPL-3',
    "category": 'Sale',
    "summary": """
        Inventory Valuation Report
    """,
    "description": """
        - Inventory Valuation Report
    """,
    "author": "AnaConEx Solutions LLC",
    "sequence": 1,
    "website": "https://www.anaconex.com/",
    "depends": ['stock', 'report_xlsx', 'product'],
    "data": [
        'security/ir.model.access.csv',
        'views/menu_report_xls.xml',
        'wizard/inventory_valuation_report_wizard.xml',
    ],

    "price": 0,
    "currency": 'USD',
    "installable": True,
    "application": True,
    "auto_install": False,
}