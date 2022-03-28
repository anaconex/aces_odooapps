# -*- coding: utf-8 -*-
from odoo import models, fields
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from dateutil.relativedelta import relativedelta
import pytz



class TimelineXlsx(models.AbstractModel):
    _name = 'report.aces_mrp_excel_reports.timeline_xls'
    _inherit = 'report.report_xlsx.abstract'
   
      
    def generate_xlsx_report(self, workbook, data, products):
        mrp_order_id = data.get('mrp_order_id')
        
        
        sheet = workbook.add_worksheet("Timeline Report")
        format1 = workbook.add_format({'font_size': 15})
        format2 = workbook.add_format({'font_size': 10, 'bold': True, 'bg_color': '#D3D3D3'})
        format3 = workbook.add_format({'font_size': 10})
        format5 = workbook.add_format({'font_size': 10, 'bold': True})
        num_format = workbook.add_format({'font_size': 10, 'num_format': '0.00'})
        format4 = workbook.add_format({'font_size': 10, 'num_format': '#,##0.00'})
        format6 = workbook.add_format({'font_size': 10, 'num_format': '#,##0.00', 'bold': True, 'bg_color': '#D3D3D3'})
        
        format1.set_align('center')
        format5.set_align('center')

        sheet.merge_range('A1:C2', 'Timeline Report', format1)
#         sheet.merge_range('A3:C3', 'Print Date : ' + str(fields.date.today()) , format5)
        headers = ["Workorder", "Workorder wise Closing", "Real Time(Spent)"]
        row = 5
        col = 0
        for header in headers:
            sheet.set_column(col, 1, 5)
            sheet.write(row, col, header, format2)
            sheet.set_column(row, col, 25)
            col += 1

        row = 6
        col = 0
        
        
        if mrp_order_id:
            mrp_order_obj = self.env['mrp.production'].browse(mrp_order_id)
            sheet.merge_range('A3:C3', 'MO # : ' + str(mrp_order_obj.name) , format5)
            sheet.merge_range('A4:C4', 'MO Creation Date : ' + str(mrp_order_obj.create_date.date()) , format5)
            workorders = self.env['mrp.workorder'].search([('production_id','=',mrp_order_id)])
            print(workorders)
            if workorders:
                for workorder in workorders:
                    for timeline in workorder.time_ids:
                        closing_datetime = str(timeline.date_end)
                        
                    duration = '{0:02.0f}:{1:02.0f}'.format(*divmod(timeline.duration * 60, 60))    
                    sheet.write(row, col+0, workorder.name, format3)
                    sheet.write(row, col+1, closing_datetime, format4)
                    sheet.write(row, col+2, duration, format3)
                    
                    row += 1
        
            row += 1
            sheet.write(row, col + 0, 'MO Final Closing Date', format2)
            sheet.write(row, col + 1, str(mrp_order_obj.date_finished), format2)
            
        

                
                