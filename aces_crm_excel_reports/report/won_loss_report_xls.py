# -*- coding: utf-8 -*-
from odoo import models
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from dateutil.relativedelta import relativedelta
import pytz



class WonLossXlsx(models.AbstractModel):
    _name = 'report.aces_crm_excel_reports.won_loss_xls'
    _inherit = 'report.report_xlsx.abstract'
   
   
    def get_lead_data(self, start_at, stop_at, status, user_id):
        start_at = datetime.strptime(start_at, '%Y-%m-%d %H:%M:%S') + relativedelta(hours=+ 5)
        stop_at = datetime.strptime(stop_at, '%Y-%m-%d %H:%M:%S') + relativedelta(hours=+ 5) 
        lead_lines = ''
        domain = []
        
        if user_id != False:
            domain = [('user_id', '=', user_id),]
                
        if status != False:
            if status == 'won':
                won_stage_id = self.env['crm.stage'].search([('is_won','=',True)], order='id desc', limit=1)
                
                if won_stage_id:
                    domain = domain + [('stage_id','=',won_stage_id.id), ('active', '=', True)]
            else:
                domain = domain + [('active', '=', False)]
                
        else:
            domain = domain + [('active', 'in', (True,False))]
            
        
        domain = domain + [('create_date', '>=', start_at), ('create_date', '<=', stop_at),]
          
        lead_lines = self.env['crm.lead'].search(domain, order="create_date asc")
        
        return lead_lines   
    
    
      
    def generate_xlsx_report(self, workbook, data, products):
        start_at = data.get('start_at')
        stop_at = data.get('stop_at')
        status = data.get('status')
        user_id = data.get('user_id')
        
        
        sheet = workbook.add_worksheet("Won Loss Report")
        format1 = workbook.add_format({'font_size': 15})
        format2 = workbook.add_format({'font_size': 10, 'bold': True, 'bg_color': '#D3D3D3'})
        format3 = workbook.add_format({'font_size': 10})
        format5 = workbook.add_format({'font_size': 10, 'bold': True})
        num_format = workbook.add_format({'font_size': 10, 'num_format': '0.00'})
        format4 = workbook.add_format({'font_size': 10, 'num_format': '#,##0.00'})
        format6 = workbook.add_format({'font_size': 10, 'num_format': '#,##0.00', 'bold': True, 'bg_color': '#D3D3D3'})
        
        format1.set_align('center')
        format5.set_align('center')

        sheet.merge_range('A1:D2', 'Won Loss Report', format1)
        sheet.merge_range('A3:D3', 'From : ' + start_at + ' To ' + stop_at , format5)
        headers = ["Sales Person", "Status", "Opportunity", "Expected Revenue"]
        row = 5
        col = 0
        for header in headers:
            sheet.set_column(col, 1, 5)
            sheet.write(row, col, header, format2)
            sheet.set_column(row, col, 18)
            col += 1

        row = 6
        col = 0
        print('---------------------------------')
#         if status != False:
#             result = self.get_lead_data(start_at, stop_at, status)
#         else:
        result = self.get_lead_data(start_at, stop_at, status, user_id) 
                   
        for line in result:
            n_status = ''
            if status != False:
                if status == 'won':
                    n_status = 'Won'
                else:
                    n_status = 'Lost'
            else:
                if line.active == True:
                    n_status = 'Won'
                else:
                    n_status = 'Lost'
                    
            sheet.write(row, col+0, line.user_id.name, format3)
            sheet.write(row, col+1, n_status, format3)
            sheet.write(row, col+2, line.name, format3)
            sheet.write(row, col+3, line.planned_revenue, format4)
            row += 1
        

                
                