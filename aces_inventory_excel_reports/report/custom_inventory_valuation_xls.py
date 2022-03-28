# -*- coding: utf-8 -*-
from odoo import models
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from dateutil.relativedelta import relativedelta
import pytz



class CustomInventoryValuationXlsx(models.AbstractModel):
    _name = 'report.aces_inventory_excel_reports.inventory_valuation_xls'
    _inherit = 'report.report_xlsx.abstract'
   
   
    def get_quants_data(self, date_at, location_id, product_ids):
        date_at = datetime.strptime(date_at, '%Y-%m-%d %H:%M:%S') + relativedelta(hours=+ 5)
        
        if location_id != False:
            quants = self.env['stock.quant'].search(
            [('in_date','<=',date_at), ('location_id','=',location_id),
             ('product_id','in',product_ids)], order="in_date asc")
        else:
            quants = self.env['stock.quant'].search(
            [('in_date','<=',date_at), ('product_id','in',product_ids)], order="in_date asc")
        
        return quants   
    
    
      
    def generate_xlsx_report(self, workbook, data, products):
        date_at = data.get('date_at')
        report_type = data.get('report_type')
        location_id = data.get('location_id')
        
        
        sheet = workbook.add_worksheet("Inventory Valuation Report")
        format1 = workbook.add_format({'font_size': 15})
        format2 = workbook.add_format({'font_size': 10, 'bold': True, 'bg_color': '#D3D3D3'})
        format3 = workbook.add_format({'font_size': 10})
        format5 = workbook.add_format({'font_size': 10, 'bold': True})
        num_format = workbook.add_format({'font_size': 10, 'num_format': '0.00'})
        format4 = workbook.add_format({'font_size': 10, 'num_format': '#,##0.00'})
        format6 = workbook.add_format({'font_size': 10, 'num_format': '#,##0.00', 'bold': True, 'bg_color': '#D3D3D3'})
        
        format1.set_align('center')
        format5.set_align('center')

        sheet.merge_range('A1:D2', 'Inventory Valuation Report', format1)
        sheet.merge_range('A3:D3', 'Inventory Date : ' + date_at , format5)
        headers = ["Product", "Onhand Qty", "Valuation", "Location"]
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
        product_ids = self.env['product.product'].search([('type','=','product')]).ids
        
        if report_type == 'location':
            result = self.get_quants_data(date_at, location_id, product_ids)
        else:
            result = self.get_quants_data(date_at, False, product_ids) 
        
                   
        for line in result:
            if line.location_id.usage == 'internal':
                sheet.write(row, col+0, line.product_id.name, format3)
                sheet.write(row, col+1, line.quantity, format3)
                sheet.write(row, col+2, line.value, format4)
                sheet.write(row, col+3, line.location_id.complete_name, format4)
                row += 1
        
            
        

                
                