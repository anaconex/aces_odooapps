from odoo import models, fields, api

class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    order_type_sale_order = fields.Selection([('fso', 'Field Service Order'), ('so', 'Sales Order')],
                                  string="Order Type", default='fso', required=True)

