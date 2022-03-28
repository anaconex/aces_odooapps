# from odoo import models, fields, api
# from odoo.exceptions import UserError
#
# class CustomPartnerLedger(models.AbstractModel):
#     _name = 'report.account.report_invoice_with_payments'
#
#     @api.model
#     def _get_report_values(self, docids, data=None):
#         #     raise UserError('You Do Not Have Access')
#
#         sessions = self.env['account.move'].browse(docids)
#         if not self.env.user.has_group('sobytek_sb_two_ent_odoo.group_cannot_edit_journal_entries'):
#             raise UserError('Not Applicable')
#         # for session in sessions:
#         #     if session.state != 'draft':
#
#         return{
#             'doc_ids': docids,
#             'doc_model': 'account.move',
#             'docs': self.env['account.move'].browse(docids),
#
#         }