# -*- coding: utf-8 -*-


from datetime import datetime, timedelta
from odoo import SUPERUSER_ID
from odoo import api, fields, models, _
from odoo.http import request


class HrAttendance(models.Model):
    _inherit = 'hr.attendance'

    def send_email(self):
        ''' Opens a wizard to compose an email, with relevant mail template loaded by default '''
        self.ensure_one()
        # template_id = self._find_mail_template()
        lang = self.env.context.get('lang')
        # template = self.env['mail.template'].browse(template_id)
        # if template.lang:
        #     lang = template._render_lang(self.ids)[self.id]
        ctx = {
            'default_model': 'hr.attendance',
            'default_res_id': self.ids[0],
            # 'default_partner_ids': self.employee_id.ids,
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True,
            'proforma': self.env.context.get('proforma', False),
            'force_email': True,
        }
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(False, 'form')],
            'view_id': False,
            'target': 'new',
            'context': ctx,
        }