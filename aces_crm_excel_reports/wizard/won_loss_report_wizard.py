# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError



class WonLossReportWizard(models.TransientModel):
    _name = 'won.loss.wizard'
    _description = 'Won Loss Report Wizard'


    start_at = fields.Datetime(string='From Date', required=True)
    stop_at = fields.Datetime(string="To Date", required=True)
    status = fields.Selection([('won','Won'),('lost','Lost')], 
                                  string="Status")
    user_id = fields.Many2one('res.users', string="Sales Person")


    def print_won_loss_xlsx(self):
        if self.start_at > self.stop_at:
            raise ValidationError(_('Invalid date !'))
        data = {
            'start_at': self.start_at,
            'stop_at': self.stop_at,
            'status': self.status,
            'user_id': self.user_id.id,
        }
        return self.env.ref('aces_crm_excel_reports.won_loss_xlsx').report_action(self, data=data)

