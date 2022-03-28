# -*- coding: utf-8 -*-

{
    'name': "AnaConEx Solutions - Attendance Email",
    'version': '14.0.2.1.0',
    'license': 'LGPL-3',
    'sequence': 1,
    'category': "Extra Tools",
    "author": "AnaConEx Solutions LLC",
    'website': 'https://www.anaconex.com',
    'summary': """
        Attendance Email
    """,
    'description': '''
              - This module adds a button to attendance view for sending an email to employees
    ''',
    'data': [
        'views/hr_attendance_view.xml'
    ],
    'depends': ['base', 'hr_attendance'],
    "price": 0,
    "currency": 'USD',
    "installable": True,
    "application": True,
    "auto_install": False,
}