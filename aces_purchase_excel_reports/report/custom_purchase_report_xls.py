# -*- coding: utf-8 -*-
from odoo import models
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from dateutil.relativedelta import relativedelta
import pytz



class CustomPurchaseXlsx(models.AbstractModel):
    _name = 'report.aces_purchase_excel_reports.custom_purchase_xls'
    _inherit = 'report.report_xlsx.abstract'
   
   
    def get_orders_data(self, start_at, stop_at, purchase_order_id, state, invoice_status):
        start_at = datetime.strptime(start_at, '%Y-%m-%d %H:%M:%S') + relativedelta(hours=+ 5)
        stop_at = datetime.strptime(stop_at, '%Y-%m-%d %H:%M:%S') + relativedelta(hours=+ 5) 
        
        if purchase_order_id != False:
            orders = self.env['purchase.order'].search(
            [('create_date', '>=', start_at), ('create_date', '<=', stop_at), 
             ('id','=',purchase_order_id),], order="id asc")
        else:
            if state != False and invoice_status == False:
                orders = self.env['purchase.order'].search(
                [('create_date', '>=', start_at), ('create_date', '<=', stop_at), ('state','=',state)], order="id asc")
            elif state == False and invoice_status != False:
                orders = self.env['purchase.order'].search(
                [('create_date', '>=', start_at), ('create_date', '<=', stop_at), ('invoice_status','=',invoice_status)], order="id asc")
            elif state != False and invoice_status != False:
                orders = self.env['purchase.order'].search(
                [('create_date', '>=', start_at), ('create_date', '<=', stop_at), 
                 ('state','=',state), ('invoice_status','=',invoice_status)], order="id asc")
            else:
                orders = self.env['purchase.order'].search(
                [('create_date', '>=', start_at), ('create_date', '<=', stop_at)], order="id asc")
        
        return orders   

    
    def get_state(self, state):
        if state == 'draft':
            state = 'RFQ'
        elif state == 'sent':
            state = 'RFQ Sent'
        elif state == 'to approve':
            state = 'To Approve'
        elif state == 'purchase':
            state = 'Purchase Order'
        elif state == 'done':
            state = 'Locked'
        else:
            state = 'Cancelled'
        return state
    

    def get_invoice_state(self, state):
        if state == 'no':
            state = 'Nothing to Bill'
        elif state == 'to invoice':
            state = 'Waiting Bills'
        else:
            state = 'Fully Billed'
        return state
        
            
    def generate_xlsx_report(self, workbook, data, products):
        # print(self.name)
        start_at = data.get('start_at')
        stop_at = data.get('stop_at')
        order_type = data.get('order_type')
        purchase_order_id = data.get('purchase_order_id')
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

        sheet.merge_range('A1:F2', 'Custom Purchase Report', format1)
        sheet.merge_range('A3:F3', 'From : ' + start_at + ' To ' + stop_at , format5)
        headers = ["PO#", "Order Date", "GRN Date", "Bill Date", "Customer", "Subtotal", "Tax", "Total", "State", "Invoice Status"]
        row = 5
        col = 0
        for header in headers:
            sheet.set_column(col, 1, 9)
            sheet.write(row, col, header, format2)
            sheet.set_column(row, col, 18)
            col += 1

        row = 6
        col = 0
        po = self.env['purchase.order']
        # print('name', self.name)
        # print('name', self.partner_id)
        if order_type == 'single_order':
            result = self.get_orders_data(start_at, stop_at, purchase_order_id, False, False)
        else:
            result = self.get_orders_data(start_at, stop_at, False, state, invoice_status) 
                   
        for line in result:
            state = self.get_state(line.state)
            # print('state --- > ', state)
            invoice_status = self.get_invoice_state(line.invoice_status)
            
            # if type(line.grn_date) != bool:
            #     sheet.write(row, col+2, line.grn_date.strftime("%Y-%m-%d"), format4)
            # elif type(line.grn_date) == bool:
            #     sheet.write(row, col+2, "Not Available", format4)
            # if type(line.grn_date) != bool:
            #     sheet.write(row, col+3, line.bill_date.strftime("%Y-%m-%d"), format4)
            # elif type(line.bill_date) == bool:
            #     sheet.write(row, col+3, "Not Available", format4)
            sheet.write(row, col+0, line.name, format3)
            sheet.write(row, col+3,'Yasir'+  line.name, format3)
            # print('->>>', line.partner_id.name)
            sheet.write(row, col+1, line.date_order.strftime("%Y-%m-%d"), format3)
            sheet.write(row, col+4, line.partner_id.name, format3)

            sheet.write(row, col+5, line.amount_untaxed, format4)
            sheet.write(row, col+6, line.amount_tax, format4)
            sheet.write(row, col+7, line.amount_total, format4)
            sheet.write(row, col+8, state, format3)
            sheet.write(row, col+9, invoice_status, format3)
            # print("DONE")
            row += 1


        amount_untaxed_tot = amount_tax_tot = amount_total_tot = 0
        for order in result:
            amount_untaxed_tot = amount_untaxed_tot + order.amount_untaxed
            amount_tax_tot = amount_tax_tot + order.amount_tax
            amount_total_tot = amount_total_tot + order.amount_total
        
        row += 1
        sheet.write(row, col + 4, 'Total', format2)
        sheet.write(row, col + 5, amount_untaxed_tot, format6)
        sheet.write(row, col + 6, amount_tax_tot, format6)
        sheet.write(row, col + 7, amount_total_tot, format6)
            
        

                
                