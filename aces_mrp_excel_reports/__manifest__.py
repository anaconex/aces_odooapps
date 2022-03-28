# -*- coding: utf-8 -*-
{
    "name": "AnaConEx Solutions - MRP Excel Reports",
    "version": '13.1.0.0',
    'license': 'AGPL-3',
    "category": 'Sale',
    "summary": """
        Manufacturing Cost/Sale Report
    """,
    "description": """
        - Manufacturing Cost/Sale Report
    """,
    "sequence": 1,
    "author": "AnaConEx Solutions LLC",
    "website": "https://www.anaconex.com/",
    "depends": ['mrp', 'report_xlsx', 'product'],
    "data": [
        'security/ir.model.access.csv',
        'views/menu_report_xls.xml',
        'wizard/cost_sale_report_wizard.xml',
        'wizard/timeline_report_wizard.xml',
    ],
    "price": 0,
    "currency": 'USD',
    "installable": True,
    "application": True,
    "auto_install": False,
}