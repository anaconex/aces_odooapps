# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError



class SaleReportWizard(models.TransientModel):
    _name = 'custom.purchase.report.wizard'
    _description = 'Purchase Report Wizard'


    start_at = fields.Datetime(string='From Date', required=True)
    stop_at = fields.Datetime(string="To Date", required=True)
    order_type = fields.Selection([('all_orders','All Orders'),('single_order','Single Order')], 
                                  string="Order Type", default='all_orders')
    purchase_order_id = fields.Many2one('purchase.order', string="Sale Order")
    state = fields.Selection([
        ('draft', 'RFQ'),
        ('sent', 'RFQ Sent'),
        ('to approve', 'To Approve'),
        ('purchase', 'Purchase Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled')], string='Status')
    invoice_status = fields.Selection([
        ('no', 'Nothing to Bill'),
        ('to invoice', 'Waiting Bills'),
        ('invoiced', 'Fully Billed'),
    ], string='Billing Status')


    def print_custom_purchases_xlsx(self):
        if self.start_at > self.stop_at:
            raise ValidationError(_('Invalid date !'))
        data = {
            'start_at': self.start_at,
            'stop_at': self.stop_at,
            'order_type': self.order_type,
            'purchase_order_id': self.purchase_order_id.id,
            'invoice_status': self.invoice_status,
            'state': self.state,
        }
        return self.env.ref('aces_purchase_excel_reports.custom_purchase_xlsx').report_action(self, data=data)

