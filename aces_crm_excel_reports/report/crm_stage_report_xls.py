# -*- coding: utf-8 -*-
from odoo import models
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from dateutil.relativedelta import relativedelta
import pytz
import re



class CrmStageXlsx(models.AbstractModel):
    _name = 'report.aces_crm_excel_reports.crm_stage_xls'
    _inherit = 'report.report_xlsx.abstract'
   
   
    def get_lead_data(self, start_at, stop_at, stage_id, user_id):
        start_at = datetime.strptime(start_at, '%Y-%m-%d %H:%M:%S') + relativedelta(hours=+ 5)
        stop_at = datetime.strptime(stop_at, '%Y-%m-%d %H:%M:%S') + relativedelta(hours=+ 5) 
        lead_lines = ''
        domain = []
        
        if user_id != False:
            domain = [('user_id', '=', user_id),]
                
        if stage_id != False:
            domain = domain + [('stage_id','=',stage_id)]
        
        domain = domain + [('create_date', '>=', start_at), ('create_date', '<=', stop_at),]
        lead_lines = self.env['crm.lead'].search(domain, order="create_date asc")
        
        return lead_lines   
    
    
    def get_log_note(self, id):
        cleantext = ''
        note_exists = self.env['mail.message'].search([('res_id','=',id)], order='id desc', limit=1)
        
        if note_exists:
            body = note_exists.body
            
            CLEANR = re.compile('<.*?>') 
            cleantext = re.sub(CLEANR, '', body)
        return cleantext
    
      
    def generate_xlsx_report(self, workbook, data, products):
        start_at = data.get('start_at')
        stop_at = data.get('stop_at')
        stage_id = data.get('stage_id')
        user_id = data.get('user_id')
        
        
        sheet = workbook.add_worksheet("CRM Stage Report")
        format1 = workbook.add_format({'font_size': 15})
        format2 = workbook.add_format({'font_size': 10, 'bold': True, 'bg_color': '#D3D3D3'})
        format3 = workbook.add_format({'font_size': 10})
        format5 = workbook.add_format({'font_size': 10, 'bold': True})
        num_format = workbook.add_format({'font_size': 10, 'num_format': '0.00'})
        format4 = workbook.add_format({'font_size': 10, 'num_format': '#,##0.00'})
        format6 = workbook.add_format({'font_size': 10, 'num_format': '#,##0.00', 'bold': True, 'bg_color': '#D3D3D3'})
        
        format1.set_align('center')
        format5.set_align('center')

        sheet.merge_range('A1:D2', 'CRM Stage Report', format1)
        sheet.merge_range('A3:D3', 'From : ' + start_at + ' To ' + stop_at , format5)
        headers = ["Salesperson", "Opportunity", "Stage", "Log Note"]
        row = 5
        col = 0
        for header in headers:
            sheet.set_column(col, 1, 5)
            sheet.write(row, col, header, format2)
            sheet.set_column(row, col, 18)
            col += 1

        row = 6
        col = 0

        result = self.get_lead_data(start_at, stop_at, stage_id, user_id) 
                   
        for line in result:
            log_note = self.get_log_note(line.id)
            
            sheet.write(row, col+0, line.user_id.name, format3)
            sheet.write(row, col+1, line.name, format3)
            sheet.write(row, col+2, line.stage_id.name, format3)
            sheet.write(row, col+3, log_note, format4)
            row += 1
            
        

                
                