# -*- coding: utf-8 -*-
from odoo import models
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from dateutil.relativedelta import relativedelta
import pytz



class SalesOrderProfitabilityXlsx(models.AbstractModel):
    _name = 'report.aces_sales_excel_reports.sales_profitability_xls'
    _inherit = 'report.report_xlsx.abstract'
   
   
    def get_order_line_data(self, start_at, stop_at, sale_order_id):
        start_at = datetime.strptime(start_at, '%Y-%m-%d %H:%M:%S') + relativedelta(hours=+ 5)
        stop_at = datetime.strptime(stop_at, '%Y-%m-%d %H:%M:%S') + relativedelta(hours=+ 5) 
        
        if sale_order_id != False:
            order_lines = self.env['sale.order.line'].search(
            [('create_date', '>=', start_at), ('create_date', '<=', stop_at), ('order_id','=',sale_order_id),
             ('state', 'in', ('sale','done'))], order="order_id asc")
        else:
            order_lines = self.env['sale.order.line'].search(
                [('create_date', '>=', start_at), ('create_date', '<=', stop_at), 
                 ('state', 'in', ('sale','done'))], order="create_date asc")
        
        return order_lines   
    
    
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
    

    def get_state_from_model(self, start_at, stop_at,state):
        if state == 'draft':
            sale_orders = self.env['sale.order'].search(
                [('create_date', '>=', start_at), ('create_date', '<=', stop_at), ('state', '=', 'draft')])
        if state == 'sent':
            sale_orders = self.env['sale.order'].search(
                [('create_date', '>=', start_at), ('create_date', '<=', stop_at), ('state', '=', 'sent')])
        if state == 'sale':
            sale_orders = self.env['sale.order'].search(
                [('create_date', '>=', start_at), ('create_date', '<=', stop_at), ('state', '=', 'sale')])
        if state == 'done':
            sale_orders = self.env['sale.order'].search(
                [('create_date', '>=', start_at), ('create_date', '<=', stop_at), ('state', '=', 'done')])
        if state == 'cancel':
            sale_orders = self.env['sale.order'].search(
                [('create_date', '>=', start_at), ('create_date', '<=', stop_at), ('state', '=', 'cancel')])
        return sale_orders

    # def get_order_type_from_model(self, start_at, stop_at, order_type):
    #     if order_type == 'fso':
    #         records = self.env['sale.order'].search(
    #             [('create_date', '>=', start_at), ('create_date', '<=', stop_at), ('order_type_sale_order', '=', 'fso')])
    #     if order_type == 'so':
    #         records = self.env['sale.order'].search(
    #             [('create_date', '>=', start_at), ('create_date', '<=', stop_at), ('order_type_sale_order', '=', 'so')])
    #     return records

    def generate_xlsx_report(self, workbook, data, products):
        start_at = data.get('start_at')
        stop_at = data.get('stop_at')
        order_type = data.get('order_type')
        state_get = data.get('state')
        order_type_sale_order_wizard = data.get('order_type_wizard')
        sale_order_id = data.get('sale_order_id')
        details_checker = data.get('detail_check')

        
        
        sheet = workbook.add_worksheet("Order Profitability Report")
        format1 = workbook.add_format({'font_size': 15})
        format2 = workbook.add_format({'font_size': 10, 'bold': True, 'bg_color': '#D3D3D3'})
        format_footer = workbook.add_format({'font_size': 10, 'bold': True, 'bg_color': '#D3D3D3'})
        format3 = workbook.add_format({'font_size': 10})
        format5 = workbook.add_format({'font_size': 10, 'bold': True})
        num_format = workbook.add_format({'font_size': 10, 'num_format': '0.00'})
        format4 = workbook.add_format({'font_size': 10, 'num_format': '#,##0.00'})
        format6 = workbook.add_format({'font_size': 10, 'num_format': '#,##0.00', 'bold': True, 'bg_color': '#D3D3D3'})
        
        format1.set_align('center')
        format3.set_align('center')
        format_footer.set_align('center')
        format5.set_align('center')

        # REPORT TYPE MENTION
        order_type_name = ''
        if order_type == 'single_order':
            result = self.get_order_line_data(start_at, stop_at, sale_order_id)
            order_type_name = 'Single Order'
        else:
            result = self.get_order_line_data(start_at, stop_at, False)
            order_type_name = 'All Orders'

        str_state = ''
        if state_get == 'draft':
            str_state = 'Quotation'
            state_result = self.get_state_from_model(start_at, stop_at, state_get)
        if state_get == 'sent':
            str_state = 'Quotation Sent'
            state_result = self.get_state_from_model(start_at, stop_at, state_get)
        if state_get == 'sale':
            str_state = 'Sales Order'
            state_result = self.get_state_from_model(start_at, stop_at, state_get)
        if state_get == 'done':
            str_state = 'Locked'
            state_result = self.get_state_from_model(start_at, stop_at, state_get)
        if state_get == 'cancel':
            str_state = 'Cancelled'
            state_result = self.get_state_from_model(start_at, stop_at, state_get)


        str_order_type_sale_oder_wizard = ''
        if order_type_sale_order_wizard == 'fso':
            str_order_type_sale_oder_wizard = 'Field Service Order'
        if order_type_sale_order_wizard == 'so':
            str_order_type_sale_oder_wizard = 'Sales Order'


        if details_checker == 'wi':
            sheet.merge_range('A4:B4', 'Report Type : ' + order_type_name, format5)
            sheet.merge_range('C4:D4', 'Records Status : ' + str_state, format5)
            sheet.merge_range('E4:F4', 'Order Type : ' + str_order_type_sale_oder_wizard, format5)
            sheet.merge_range('G4:H4', 'Records Type : ' + 'With Detail', format5)
            sheet.merge_range('A1:I2', 'Order Profitability Report', format1)
            sheet.merge_range('A3:I3', 'From : ' + start_at + ' To ' + stop_at , format5)
            # HEADER SECTION
            headers = ["SO#", "Customer", "Product", "Sale Price", "Cost Price", "Tax", "Difference",  "State", "Invoice Status"]
            row = 5
            col = 0
            for header in headers:
                sheet.set_column(col, 1, 10)
                sheet.write(row, col, header, format2)
                sheet.set_column(row, col, 18)
                col += 1

            row = 6
            col = 0
            sales_price_calc=0
            cost_price_calc=0
            tax_calc=0
            differece_calc=0
            sale_order_records = self.env['sale.order'].search([('state', '=', state_get), ('order_type_sale_order', '=', order_type_sale_order_wizard)])
            if sale_order_records:
                for record in sale_order_records:
                    # if record.state == state_get and record.order_type_sale_order == order_type_sale_order_wizard:
                    print(record.name)
                    #     print(record.order_type_sale_order)
                    #     print(record.state)
                    for line in record.order_line:
                        invoice_status = self.get_invoice_state(line.invoice_status)
                        # print(line.product_id.name)
                        # print(line.name)
                        sheet.write(row, col+0, record.name, format3)
                        sheet.write(row, col+1, record.partner_id.name, format3)
                        sheet.write(row, col+2, line.product_id.name, format3)
                        sheet.write(row, col+3, line.price_subtotal, format3)
                        sheet.write(row, col+4, line.product_id.standard_price * line.product_uom_qty, format3)
                        sheet.write(row, col+5, line.price_total - line.price_subtotal, format3)
                        sheet.write(row, col+6, line.price_subtotal - (line.product_id.standard_price * line.product_uom_qty), format3)
                        sheet.write(row, col+7, str_state, format3)
                        sheet.write(row, col+8, invoice_status, format3)
                        row += 1
                        sales_price_calc += line.price_subtotal
                        cost_price_calc += (line.product_id.standard_price * line.product_uom_qty)
                        tax_calc += (line.price_total - line.price_subtotal)
                        differece_calc += line.price_subtotal - (line.product_id.standard_price * line.product_uom_qty)
                    sheet.write(row, col + 2, 'Total', format_footer)
                    sheet.write(row, col + 3, sales_price_calc, format_footer)
                    sheet.write(row, col + 4, cost_price_calc, format_footer)
                    sheet.write(row, col + 5, tax_calc, format_footer)
                    sheet.write(row, col + 6, differece_calc, format_footer)
            else:
                row+=1
                sheet.write(row, col + 2, 'Total', format_footer)
                sheet.write(row, col + 3, '0', format_footer)
                sheet.write(row, col + 4, '0', format_footer)
                sheet.write(row, col + 5, '0', format_footer)
                sheet.write(row, col + 6, '0', format_footer)


            # for record in state_result:
            #     if record.state == state_get and record.order_type_sale_order == order_type_sale_order_wizard:
            #         print(record.name)
            #         print(record.order_type_sale_order)
            #         print(record.state)
            #         for line in record.order_line:
            #             invoice_status = self.get_invoice_state(line.invoice_status)
            #             # print(line.product_id.name)
            #             # print(line.name)
            #             sheet.write(row, col+0, record.name, format3)
            #             sheet.write(row, col+1, record.partner_id.name, format3)
            #             sheet.write(row, col+2, line.product_id.name, format3)
            #             sheet.write(row, col+3, line.price_subtotal, format4)
            #             sheet.write(row, col+4, line.product_id.standard_price * line.product_uom_qty, format4)
            #             sheet.write(row, col+5, line.price_total - line.price_subtotal, format4)
            #             sheet.write(row, col+6, line.price_subtotal - (line.product_id.standard_price * line.product_uom_qty), format4)
            #             sheet.write(row, col+7, str_state, format3)
            #             sheet.write(row, col+8, invoice_status, format3)
            #             row += 1

                    #     sale_price_tot = cost_price_tot = tax_tot = difference_tot = 0
                    #     for line in result:
                    #         sale_price_tot = sale_price_tot + line.price_subtotal
                    #         cost_price_tot = cost_price_tot + (line.product_id.standard_price * line.product_uom_qty)
                    #         tax_tot = tax_tot + (line.price_total - line.price_subtotal)
                    #     difference_tot = sale_price_tot - cost_price_tot
                    #
                    # row += 1
                    # sheet.write(row, col + 2, 'Total', format2)
                    # sheet.write(row, col + 3, sale_price_tot, format6)
                    # sheet.write(row, col + 4, cost_price_tot, format6)
                    # sheet.write(row, col + 5, tax_tot, format6)
                    # sheet.write(row, col + 6, difference_tot, format6)

        if details_checker == 'woi':
            sheet.write(3, 0, 'Report Type : ' + order_type_name, format5)
            sheet.write(3, 1, 'Records Status : ' + str_state, format5)
            sheet.write(3, 2, 'Order Type : ' + str_order_type_sale_oder_wizard, format5)
            sheet.write(3, 3, 'Records Type : ' + 'Without Detail', format5)
            sheet.merge_range('A1:D2', 'Order Profitability Report', format1)
            sheet.merge_range('A3:D3', 'From : ' + start_at + ' To ' + stop_at , format5)
            headers = ["SO#", "Cost", "Tax", "Sale"]
            row = 5
            col = 0
            for header in headers:
                sheet.set_column(col, 1, 10)
                sheet.write(row, col, header, format2)
                sheet.set_column(row, col, 18)
                col += 1

            sheet.set_column(3, 0, 30)
            sheet.set_column(3, 1, 30)
            sheet.set_column(3, 2, 30)
            sheet.set_column(3, 3, 30)

            sale_order_records = self.env['sale.order'].search([('state', '=', state_get),('order_type_sale_order', '=', order_type_sale_order_wizard)])
            row = 6
            col = 0
            cost_calc=0
            tax_calc=0
            sale_calc=0
            if sale_order_records:
                for records in sale_order_records:
                    sheet.write(row, col + 0, records.name, format3)
                    sheet.write(row, col + 1, records.amount_untaxed, format3)
                    sheet.write(row, col + 2, records.amount_tax, format3)
                    sheet.write(row, col + 3, records.amount_total, format3)
                    row += 1
                    cost_calc += records.amount_untaxed
                    tax_calc += records.amount_tax
                    sale_calc += records.amount_total
                sheet.write(row, col + 0, 'Total', format_footer)
                sheet.write(row, col + 1, cost_calc, format_footer)
                sheet.write(row, col + 2, tax_calc, format_footer)
                sheet.write(row, col + 3, sale_calc, format_footer)
            else:
                row+=1
                sheet.write(row, col + 0, 'Total', format_footer)
                sheet.write(row, col + 1, '0', format_footer)
                sheet.write(row, col + 2, '0', format_footer)
                sheet.write(row, col + 3, '0', format_footer)
            # sheet.merge_range('D4', 'Order Type : ' + str_order_type_sale_oder_wizard, format5)

            # for record in state_result:
            #     if record.state == state_get and record.order_type_sale_order == order_type_sale_order_wizard:
            #         print(record.name)
            #         print(record.order_type_sale_order)
            #         print(record.state)
            #         for line in record.order_line:
            #             invoice_status = self.get_invoice_state(line.invoice_status)
            #             # print(line.product_id.name)
            #             # print(line.name)
            #             sheet.write(row, col+0, record.name, format3)
            #             sheet.write(row, col+1, record.partner_id.name, format3)
            #             sheet.write(row, col+2, line.product_id.name, format3)
            #             sheet.write(row, col+3, line.price_subtotal, format4)
            #             sheet.write(row, col+4, line.product_id.standard_price * line.product_uom_qty, format4)
            #             sheet.write(row, col+5, line.price_total - line.price_subtotal, format4)
            #             sheet.write(row, col+6, line.price_subtotal - (line.product_id.standard_price * line.product_uom_qty), format4)
            #             sheet.write(row, col+7, str_state, format3)
            #             sheet.write(row, col+8, invoice_status, format3)
            #             row += 1




                # for line in result:
                #     sheet.write(row, col+0, line.order_id.name, format3)
                #     sheet.write(row, col+1, line.order_id.partner_id.name, format3)
                #     sheet.write(row, col+2, line.product_id.name, format3)
                #     sheet.write(row, col+3, line.price_subtotal, format4)
                #     sheet.write(row, col+4, line.product_id.standard_price * line.product_uom_qty, format4)
                #     sheet.write(row, col+5, line.price_total - line.price_subtotal, format4)
                #     sheet.write(row, col+6, line.price_subtotal - (line.product_id.standard_price * line.product_uom_qty), format4)
                #     sheet.write(row, col+7, line.state, format3)
                #     # sheet.write(row, col+8, invoice_status, format3)
                #     row += 1
                # print(record.state)
                # print(record.name)

            # if line.state == state:






            # state = self.get_state(line.state)
            # invoice_status = self.get_invoice_state(line.invoice_status)
            #
            # sheet.write(row, col+0, line.order_id.name, format3)
            # sheet.write(row, col+1, line.order_id.partner_id.name, format3)
            # sheet.write(row, col+2, line.product_id.name, format3)
            # sheet.write(row, col+3, line.price_subtotal, format4)
            # sheet.write(row, col+4, line.product_id.standard_price * line.product_uom_qty, format4)
            # sheet.write(row, col+5, line.price_total - line.price_subtotal, format4)
            # sheet.write(row, col+6, line.price_subtotal - (line.product_id.standard_price * line.product_uom_qty), format4)
            # sheet.write(row, col+7, state, format3)
            # sheet.write(row, col+8, invoice_status, format3)
            # row += 1














        # for line in result:
        #     state = self.get_state(line.state)
        #     invoice_status = self.get_invoice_state(line.invoice_status)
        #
        #     sheet.write(row, col+0, line.order_id.name, format3)
        #     sheet.write(row, col+1, line.order_id.partner_id.name, format3)
        #     sheet.write(row, col+2, line.product_id.name, format3)
        #     sheet.write(row, col+3, line.price_subtotal, format4)
        #     sheet.write(row, col+4, line.product_id.standard_price * line.product_uom_qty, format4)
        #     sheet.write(row, col+5, line.price_total - line.price_subtotal, format4)
        #     sheet.write(row, col+6, line.price_subtotal - (line.product_id.standard_price * line.product_uom_qty), format4)
        #     sheet.write(row, col+7, state, format3)
        #     sheet.write(row, col+8, invoice_status, format3)
        #     row += 1
        #
        # sale_price_tot = cost_price_tot = tax_tot = difference_tot = 0
        #
        # for line in result:
        #     sale_price_tot = sale_price_tot + line.price_subtotal
        #     cost_price_tot = cost_price_tot + (line.product_id.standard_price * line.product_uom_qty)
        #     tax_tot = tax_tot + (line.price_total - line.price_subtotal)
        # difference_tot = sale_price_tot - cost_price_tot
        #
        # row += 1
        # sheet.write(row, col + 2, 'Total', format2)
        # sheet.write(row, col + 3, sale_price_tot, format6)
        # sheet.write(row, col + 4, cost_price_tot, format6)
        # sheet.write(row, col + 5, tax_tot, format6)
        # sheet.write(row, col + 6, difference_tot, format6)
            
        

                
                