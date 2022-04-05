{
    'name': "AnaConeEx Solutions - Products Inventory Portal",
    'version': '14.0.2.1.0',
    'license': 'LGPL-3',
    'sequence': 1,
    'summary': """
           User can view products along their inventory from portal
    """,
    'description': """
        - User can view products along their inventory from portal   
    """,
    "author": "AnaConEx Solutions LLC",
    "website": "https://www.anaconex.com/",
    'category': 'Inventory',
    # any module necessary for this one to work correctly
    'depends': ['product', 'stock', 'portal','rating','web','web_tour','digest','base','purchase_stock'],
    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/product_product_view.xml',
        'views/product_inventory_template.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
#         'demo/demo.xml',
    ],
    "price": 100,
    "currency": 'USD',
    "installable": True,
    "application": True,
    "auto_install": False,
}
