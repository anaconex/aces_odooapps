# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError



class SaleReportWizard(models.TransientModel):
    _name = 'custom.sale.report.wizard'
    _description = 'Sale Report Wizard'


    start_at = fields.Datetime(string='From Date', required=True)
    stop_at = fields.Datetime(string="To Date", required=True)
    order_type = fields.Selection([('all_orders','All Orders'),('single_order','Single Order')], 
                                  string="Order Type", default='all_orders')
    sale_order_id = fields.Many2one('sale.order', string="Sale Order")
    state = fields.Selection([
        ('draft', 'Quotation'),
        ('sent', 'Quotation Sent'),
        ('sale', 'Sales Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled'),
        ], string='Status')
    invoice_status = fields.Selection([
        ('invoiced', 'Fully Invoiced'),
        ('to invoice', 'To Invoice'),
        ('no', 'Nothing to Invoice')
        ], string='Invoice Status')


    def print_custom_sales_xlsx(self):
        if self.start_at > self.stop_at:
            raise ValidationError(_('Invalid date !'))
        data = {
            'start_at': self.start_at,
            'stop_at': self.stop_at,
            'order_type': self.order_type,
            'sale_order_id': self.sale_order_id.id,
            'invoice_status': self.invoice_status,
            'state': self.state,
        }
        return self.env.ref('aces_sales_excel_reports.custom_sale_xlsx').report_action(self, data=data)

