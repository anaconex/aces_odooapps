# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError



class OrderProfitabilityReportWizard(models.TransientModel):
    _name = 'order.profitability.wizard'
    _description = 'Order Profitability Sale Report Wizard'


    start_at = fields.Datetime(string='From Date', required=True)
    stop_at = fields.Datetime(string="To Date", required=True)
    order_type = fields.Selection([('all_orders','All Orders'),('single_order','Single Order')], 
                                  string="Order Type", default='all_orders')
    sale_order_id = fields.Many2one('sale.order', string="Sale Order")
    order_type_sale_order_wizard = fields.Selection([('fso', 'Field Service Order'), ('so', 'Sales Order')],
                                  string="Order Type", default='fso', required=True)
    detail_checker = fields.Selection([('wi', 'With Detail'), ('woi', 'Without Detail')],
                                             string="Records Type", default='with_info', required=True)
    state_wizard = fields.Selection([
        ('draft', 'Quotation'),
        ('sent', 'Quotation Sent'),
        ('sale', 'Sales Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled'),
        ], string='Status')


    def print_sales_profitability_xlsx(self):
        if self.start_at > self.stop_at:
            raise ValidationError(_('Invalid date !'))
        data = {
            'start_at': self.start_at,
            'stop_at': self.stop_at,
            'order_type': self.order_type,
            'sale_order_id': self.sale_order_id.id,
            'state': self.state_wizard,
            'order_type_wizard': self.order_type_sale_order_wizard,
            'detail_check': self.detail_checker,
        }
        return self.env.ref('aces_sales_excel_reports.sales_profitability_xlsx').report_action(self, data=data)

