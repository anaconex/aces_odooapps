# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError



class SaleReportWizard(models.TransientModel):
    _name = 'mrp.cost.sale.report.wizard'
    _description = 'MRP Cost Sale Report Wizard'


    start_at = fields.Datetime(string='From Date')
    stop_at = fields.Datetime(string="To Date")
    order_type = fields.Selection([('all_orders','All Orders'),('single_order','Single Order')], 
                                  string="Order Type", default='all_orders')
    mrp_order_id = fields.Many2one('mrp.production', string="Manufacturing Order")


    def print_mrp_cost_sales_xlsx(self):
        if self.start_at > self.stop_at:
            raise ValidationError(_('Invalid date !'))
        data = {
            'start_at': self.start_at,
            'stop_at': self.stop_at,
            'order_type': self.order_type,
            'mrp_order_id': self.mrp_order_id.id,
        }
        return self.env.ref('aces_mrp_excel_reports.mrp_cost_sale_xlsx').report_action(self, data=data)

