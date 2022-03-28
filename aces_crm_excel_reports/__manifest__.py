# -*- coding: utf-8 -*-
{
    "name": "AnaConEx Solutions - CRM Excel Reports",
    "version": '13.1.0.0',
    'license': 'AGPL-3',
    "category": 'API',
    "summary": """
        CRM Won/Loss Report and CRM Stage Report
    """,
    "description": """
        - CRM Won/Loss Report and CRM Stage Report, This module requires report_xlsx module as its dependency
        
    """,
    "author": "AnaConEx Solutions LLC",
    "sequence": 1,
    "website": "https://www.anaconex.com/",
    "depends": ['crm', 'report_xlsx'],
    "data": [
        'security/ir.model.access.csv',
        'views/menu_report_xls.xml',
        'wizard/won_loss_report_wizard.xml',
        'wizard/stages_report_wizard.xml',
    ],
    
    "price": 0,
    "currency": 'USD',
    "installable": True,
    "application": True,
    "auto_install": False,
}
