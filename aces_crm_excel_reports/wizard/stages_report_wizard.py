# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError



class CrmStageReportWizard(models.TransientModel):
    _name = 'crm.stages.report.wizard'
    _description = 'CRM Stage Report Wizard'


    start_at = fields.Datetime(string='From Date', required=True)
    stop_at = fields.Datetime(string="To Date", required=True)
    user_id = fields.Many2one('res.users', string="Salesperson")
    stage_id = fields.Many2one('crm.stage', string="Stage")

    
    def print_crm_stage_xlsx(self):
        if self.start_at > self.stop_at:
            raise ValidationError(_('Invalid date !'))
        data = {
            'start_at': self.start_at,
            'stop_at': self.stop_at,
            'user_id': self.user_id.id,
            'stage_id': self.stage_id.id,
        }
        return self.env.ref('aces_crm_excel_reports.crm_stage_xlsx').report_action(self, data=data)

