from odoo import models, fields, api

class AccountMoveLineInherit(models.Model):
    _inherit = 'account.move.line'

class AccountMoveInherit(models.Model):
    _inherit = 'account.move'

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(AccountMoveInherit, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)

        if res.get('toolbar', False) and res.get('toolbar').get('print', False):
            reports = res.get('toolbar').get('print')

            if self.env.user.has_group('aces_access_rules_for_users_in_journal_entries.group_cannot_access_print_action'):
                # print("TRUEEEE")
                res['toolbar']['print'] = []
                # print("DONE")

        return res

