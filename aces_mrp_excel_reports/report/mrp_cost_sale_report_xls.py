# -*- coding: utf-8 -*-
from odoo import models
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from dateutil.relativedelta import relativedelta
import pytz



class MrpCostSaleXlsx(models.AbstractModel):
    _name = 'report.aces_mrp_excel_reports.mrp_cost_sale_xls'
    _inherit = 'report.report_xlsx.abstract'
   
   
    def get_mrp_orders_data(self, start_at, stop_at, mrp_order_id):
        if start_at and stop_at:
            start_at = datetime.strptime(start_at, '%Y-%m-%d %H:%M:%S') + relativedelta(hours=+ 5)
            stop_at = datetime.strptime(stop_at, '%Y-%m-%d %H:%M:%S') + relativedelta(hours=+ 5) 
        
        if mrp_order_id != False:
            mrp_orders = self.env['mrp.production'].search([('id','=',mrp_order_id)], order="id asc")
        else:
            mrp_orders = self.env['mrp.production'].search(
                [('create_date', '>=', start_at), ('create_date', '<=', stop_at)], order="create_date asc")
        
        return mrp_orders   
    
    
    def get_bom_product_cost(self, mo_id):
        raw_material_moves = []
        total_cost = total_qty = sale_price = 0
        ProductProduct = self.env['product.product']
        
        query_str = """SELECT sm.product_id, sm.bom_line_id, abs(SUM(svl.quantity)), abs(SUM(svl.value))
                         FROM stock_move AS sm
                   INNER JOIN stock_valuation_layer AS svl ON svl.stock_move_id = sm.id
                        WHERE sm.raw_material_production_id in %s AND sm.state != 'cancel' AND sm.product_qty != 0 AND scrapped != 't'
                     GROUP BY sm.bom_line_id, sm.product_id"""
        self.env.cr.execute(query_str, (tuple([mo_id]), ))
        for product_id, bom_line_id, qty, cost in self.env.cr.fetchall():
            raw_material_moves.append({
                'qty': qty,
                'cost': cost,
#                 'product_id': ProductProduct.browse(product_id),
                'bom_line_id': bom_line_id
            })
            total_cost += cost
            total_qty = qty
            product_id = ProductProduct.browse(product_id)
            sale_price += product_id.lst_price
            
        return [total_cost, total_qty, sale_price*total_qty]
    
      
    def generate_xlsx_report(self, workbook, data, products):
        start_at = data.get('start_at')
        stop_at = data.get('stop_at')
        order_type = data.get('order_type')
        mrp_order_id = data.get('mrp_order_id')
        
        
        
        sheet = workbook.add_worksheet("MRP Cost Sale Report")
        format1 = workbook.add_format({'font_size': 15})
        format2 = workbook.add_format({'font_size': 10, 'bold': True, 'bg_color': '#D3D3D3'})
        format3 = workbook.add_format({'font_size': 10})
        format5 = workbook.add_format({'font_size': 10, 'bold': True})
        num_format = workbook.add_format({'font_size': 10, 'num_format': '0.00'})
        format4 = workbook.add_format({'font_size': 10, 'num_format': '#,##0.00'})
        format6 = workbook.add_format({'font_size': 10, 'num_format': '#,##0.00', 'bold': True, 'bg_color': '#D3D3D3'})
        
        format1.set_align('center')
        format5.set_align('center')

        sheet.merge_range('A1:F2', 'MRP Cost Sale Report', format1)
        
        if start_at and stop_at:
            sheet.merge_range('A3:F3', 'From : ' + start_at + ' To ' + stop_at , format5)
        
        headers = ["MO#", "Create Date", "Product", "Quantity", "Cost Price", "Sale Price"]
        row = 5
        col = 0
        for header in headers:
            sheet.set_column(col, 1, 7)
            sheet.write(row, col, header, format2)
            sheet.set_column(row, col, 18)
            col += 1

        row = 6
        col = 0

        order_type_name = ''
        
        if order_type == 'single_order':
            result = self.get_mrp_orders_data(False, False, mrp_order_id)
            order_type_name = 'Single Order'
        else:
            result = self.get_mrp_orders_data(start_at, stop_at, False) 
            order_type_name = 'All Orders'
            
        sheet.merge_range('A4:F4', 'Report Type : ' + order_type_name, format5)
        
                   
        for line in result:
            get_bom_product_cost = self.get_bom_product_cost(line.id)
            cost_price = get_bom_product_cost[0]
            qty = get_bom_product_cost[1]
            sale_price = get_bom_product_cost[2]
            
            sheet.write(row, col+0, line.name, format3)
            sheet.write(row, col+1, str(line.create_date.date()), format3)
            sheet.write(row, col+2, line.product_id.name, format3)
            sheet.write(row, col+3, qty, format4)
            sheet.write(row, col+4, cost_price, format4)
            sheet.write(row, col+5, sale_price, format4)
            row += 1
        
#         sale_price_tot = cost_price_tot = tax_tot = difference_tot = 0
#         
#         for line in result:
#             sale_price_tot = sale_price_tot + line.price_subtotal
#             cost_price_tot = cost_price_tot + (line.product_id.standard_price * line.product_uom_qty)
#             tax_tot = tax_tot + (line.price_total - line.price_subtotal)
#         difference_tot = sale_price_tot - cost_price_tot
#                 
#         row += 1
#         sheet.write(row, col + 2, 'Total', format2)
#         sheet.write(row, col + 3, sale_price_tot, format6)
#         sheet.write(row, col + 4, cost_price_tot, format6)
#         sheet.write(row, col + 5, tax_tot, format6)
#         sheet.write(row, col + 6, difference_tot, format6)
            
        

                
                