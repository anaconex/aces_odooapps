# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError



class TimeLineReportWizard(models.TransientModel):
    _name = 'timeline.report.wizard'
    _description = 'Timeline Report Wizard'


    mrp_order_id = fields.Many2one('mrp.production', string="MRP Order")


    def print_timeline_report_xlsx(self):
        data = {
            'mrp_order_id': self.mrp_order_id.id,
        }
        return self.env.ref('aces_mrp_excel_reports.timeline_xlsx').report_action(self, data=data)

