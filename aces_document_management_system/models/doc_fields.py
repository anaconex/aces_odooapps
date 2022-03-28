from odoo import models, fields, api, _
from datetime import datetime, date, time, timedelta

class DocumentSystem(models.Model):
    _name = 'document.manager'
    _inherit = ['mail.thread', 'mail.activity.mixin']  # For Chatter
    _rec_name = 'doc_name'

    @api.model
    def send_emails(self):
        rn = datetime.now()
        current_time = rn.strftime('%I:%M:%S')

        # temp = datetime.datetime.now() + datetime.timedelta(days=1)
        # print(temp)
        print("!!..HELLO CRON JOBS..!!")
        # print("Current Time =", current_time)
        records = self.env['document.manager'].search([])
        for recs in records:
            print("Email Sending")
            recs.send_backend_email()
            print("Email Sent")


        # for rec in records:
        #     for j in rec.employee_ids:
        #         print(j.work_email)
        # for rec in records:
        #     print("Expiry Date =", rec.doc_exp_date)
        #     next_day = datetime.now() + timedelta(days=1)
        #     if next_day < rec.doc_exp_date:
        #         print('Not Exp',next_day)
        #     else:
        #         print("Expired", rec.doc_exp_date)

    def send_backend_email(self):
        records = self.env['document.manager'].search([])
        for rec in records:
            for m2m in rec.employee_ids:
                ctx={}
                email_lst = [m2m.work_email]
                if email_lst:
                    ctx['email_to'] = ','.join(email for email in email_lst if email)
                    ctx['email_from'] = self.env.user.company_id.email
                    ctx['send_email'] = True
                    ctx['attendee'] = m2m.name
                    template = self.env.ref('aces_document_management_system.email_template_document_manager')
                    template.with_context(ctx).send_mail(self.id, force_send = True, raise_exception = False)
                    print('Email Sent Successfully')

    @api.model
    def create(self, vals):
        if vals.get('doc_name_seq', _('New')) == _('New'):
            vals['doc_name_seq'] = self.env['ir.sequence'].next_by_code('document.manager.sequence') or _('New')
        result = super(DocumentSystem, self).create(vals)  # METHOD TO CREATE SUPER METHOD
        return result

    doc_name_seq = fields.Char(string='Document ID', required=True, copy=False, readonly=True, index=True,
                               default=lambda self: _('New'))
    doc_name = fields.Char(string="Document Name", required=True, tracking=True)
    employee_ids = fields.Many2many('hr.employee', string='Employee IDs', tracking=True )
    doc_exp_date = fields.Datetime(string='Expiry Date', tracking=True)
    doc_rem_date = fields.Datetime(string='Reminder Date', tracking=True)
    doc_description = fields.Text(string="Document Description", tracking=True)
    documents = fields.Binary(string="Document", tracking=True)
    documents_one2many = fields.One2many("document.manager.lines", 'documents_many2one', string="Documents One 2 Many")

class DocumentSystemLines(models.Model):
    _name = "document.manager.lines"

    documents_name_line = fields.Binary(string="Document", tracking=True)
    file_name = fields.Char('File Name')
    doc_exp_date_line = fields.Datetime(string='Expiry Date', tracking=True)
    documents_many2one = fields.Many2one("document.manager", string="Document Lines")

