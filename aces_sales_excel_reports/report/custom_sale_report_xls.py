# -*- coding: utf-8 -*-
from odoo import models
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from dateutil.relativedelta import relativedelta
import pytz



class CustomSalesXlsx(models.AbstractModel):
    _name = 'report.aces_sales_excel_reports.custom_sale_xls'
    _inherit = 'report.report_xlsx.abstract'
   
   
    def get_orders_data(self, start_at, stop_at, sale_order_id, state, invoice_status):
        start_at = datetime.strptime(start_at, '%Y-%m-%d %H:%M:%S') + relativedelta(hours=+ 5)
        stop_at = datetime.strptime(stop_at, '%Y-%m-%d %H:%M:%S') + relativedelta(hours=+ 5) 
        
        print('===========state',state)
        if sale_order_id != False:
            orders = self.env['sale.order'].search(
            [('create_date', '>=', start_at), ('create_date', '<=', stop_at), 
             ('id','=',sale_order_id)], order="id asc")
        else:
            if state != False and invoice_status == False:
                orders = self.env['sale.order'].search(
                [('create_date', '>=', start_at), ('create_date', '<=', stop_at), ('state','=',state)], order="id asc")
            elif state == False and invoice_status != False:
                orders = self.env['sale.order'].search(
                [('create_date', '>=', start_at), ('create_date', '<=', stop_at), ('invoice_status','=',invoice_status)], order="id asc")
            elif state != False and invoice_status != False:
                orders = self.env['sale.order'].search(
                [('create_date', '>=', start_at), ('create_date', '<=', stop_at), 
                 ('state','=',state), ('invoice_status','=',invoice_status)], order="id asc")
            else:
                orders = self.env['sale.order'].search(
                [('create_date', '>=', start_at), ('create_date', '<=', stop_at)], order="id asc")
        
        return orders   
    
    
    def get_state(self, state):
        if state == 'draft':
            state = 'Quotation'
        elif state == 'sent':
            state = 'Quotation Sent'
        elif state == 'sale':
            state = 'Sales Order'
        elif state == 'done':
            state = 'Locked'
        else:
            state = 'Cancelled'
        return state
    

    def get_invoice_state(self, state):
        if state == 'invoiced':
            state = 'Fully Invoiced'
        elif state == 'to invoice':
            state = 'To Invoice'
        else:
            state = 'Nothing to Invoice'
        return state
        
            
    def generate_xlsx_report(self, workbook, data, products):
        start_at = data.get('start_at')
        stop_at = data.get('stop_at')
        order_type = data.get('order_type')
        sale_order_id = data.get('sale_order_id')
        state = data.get('state')
        invoice_status = data.get('invoice_status')
        
        
        
        sheet = workbook.add_worksheet("Custom Sale Report")
        format1 = workbook.add_format({'font_size': 15})
        format2 = workbook.add_format({'font_size': 10, 'bold': True, 'bg_color': '#D3D3D3'})
        format3 = workbook.add_format({'font_size': 10})
        format5 = workbook.add_format({'font_size': 10, 'bold': True})
        num_format = workbook.add_format({'font_size': 10, 'num_format': '0.00'})
        format4 = workbook.add_format({'font_size': 10, 'num_format': '#,##0.00'})
        format6 = workbook.add_format({'font_size': 10, 'num_format': '#,##0.00', 'bold': True, 'bg_color': '#D3D3D3'})
        
        format1.set_align('center')
        format5.set_align('center')

        sheet.merge_range('A1:F2', 'Custom Sale Report', format1)
        sheet.merge_range('A3:F3', 'From : ' + start_at + ' To ' + stop_at , format5)
        headers = ["SO#", "Order Date", "Customer", "Subtotal", "Tax", "Total", "State", "Invoice Status"]
        row = 5
        col = 0
        for header in headers:
            sheet.set_column(col, 1, 9)
            sheet.write(row, col, header, format2)
            sheet.set_column(row, col, 18)
            col += 1

        row = 6
        col = 0
        print('---------------------------------')
        print(sale_order_id)
        if order_type == 'single_order':
            result = self.get_orders_data(start_at, stop_at, sale_order_id, False, False)
        else:
            result = self.get_orders_data(start_at, stop_at, False, state, invoice_status) 
                   
        for line in result:
            state = self.get_state(line.state)
            invoice_status = self.get_invoice_state(line.invoice_status)
            
            sheet.write(row, col+0, line.name, format3)
            sheet.write(row, col+1, line.date_order.strftime("%Y-%m-%d"), format3)
            sheet.write(row, col+2, line.partner_id.name, format3)
            sheet.write(row, col+3, line.amount_untaxed, format4)
            sheet.write(row, col+4, line.amount_tax, format4)
            sheet.write(row, col+5, line.amount_total, format4)
            sheet.write(row, col+6, state, format3)
            sheet.write(row, col+7, invoice_status, format3)
            row += 1


        amount_untaxed_tot = amount_tax_tot = amount_total_tot = 0
        for order in result:
            amount_untaxed_tot = amount_untaxed_tot + order.amount_untaxed
            amount_tax_tot = amount_tax_tot + order.amount_tax
            amount_total_tot = amount_total_tot + order.amount_total
        
        row += 1
        sheet.write(row, col + 2, 'Total', format2)
        sheet.write(row, col + 3, amount_untaxed_tot, format6)
        sheet.write(row, col + 4, amount_tax_tot, format6)
        sheet.write(row, col + 5, amount_total_tot, format6)
            
        

                
                