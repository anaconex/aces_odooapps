{
    "name": "AnaConEx Solutions - Document Management System",
    'version': '14.0.2.1.0',
    'license': 'LGPL-3',
    'sequence': 1,
    "category": "API",
    "summary": "Module to manage documents",
    "description": """
        Module to manage documents
    """,
    "author": "AnaConEx Solutions LLC",
    "website": "https://www.anaconex.com/",
    "depends": ['base','mail','hr'],
    "data": [
        'security/ir.model.access.csv',
        'data/cron_jobs.xml',
        'data/email_template.xml',
        'data/sequence.xml',
        'views/doc_views.xml',
    ],
    "price": 0,
    "currency": 'PKR',
    "installable": True,
    "application": True,
    "auto_install": False,
}