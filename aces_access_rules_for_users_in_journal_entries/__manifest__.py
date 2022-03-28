{
    "name": "AnaConEx Solutions - Access Rules For Journal Entries",
    'version': '14.0.2.1.0',
    'sequence': 5,
    "summary": "Access rules for users of journal entries",
    "description": """
    - Access rules for users of journal entries
    """,
    'category': '',
    "author": "AnaConEx Solutions LLC",
    "website": "https://www.anaconex.com/",
    'license': 'AGPL-3',
    'depends': ['base','stock','account','web'],
    'data': [
        'security/security.xml',
        'data/button_for_defined_groups.xml',
    ],
    'demo': [],
    'qweb': [
        "static/src/xml/base.xml",
    ],
    "price": 0,
    "currency": 'USD',
    'installable': True,
    'application': True,
    'auto_install': False,
}
