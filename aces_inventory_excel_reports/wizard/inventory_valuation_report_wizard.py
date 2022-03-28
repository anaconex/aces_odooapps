# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError



class InventoryValuationReportWizard(models.TransientModel):
    _name = 'custom.inventory.valuation.wizard'
    _description = 'Custom Inventory Valuation Report Wizard'


    date_at = fields.Datetime(string='Inventory Date', required=True)
    report_type = fields.Selection([('all_inventory','All Inventory'),('location','Location')], 
                                  string="Report Type", default='all_inventory')
    location_id = fields.Many2one('stock.location', string="Location")


    def print_custom_inventory_valuation_xlsx(self):
        data = {
            'date_at': self.date_at,
            'report_type': self.report_type,
            'location_id': self.location_id.id,
        }
        return self.env.ref('aces_inventory_excel_reports.custom_inventory_valuation_xlsx').report_action(self, data=data)

