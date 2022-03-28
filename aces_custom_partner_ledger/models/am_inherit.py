from odoo import models, fields, api

class AccountMoveInherit(models.Model):
    _inherit = 'account.move'

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(AccountMoveInherit, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar,
                                                              submenu=submenu)

        if res.get('toolbar', False) and res.get('toolbar').get('action', False):
            if self.env.user.has_group('aces_custom_partner_ledger.group_cannot_access_print_action'):
                res['toolbar']['action'] = []

        return res