# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

        

class ProductTemplate(models.Model):
    _inherit = 'product.template'   
    
    
    def action_discountinued(self):
        product_ids = self.env['product.product'].search([('product_tmpl_id','=',self.id)])
        if product_ids:
            for product_id in product_ids:
                product_id.action_discountinued()
                
        self.is_discountinued = True
    
    def action_countinued(self):
        product_ids = self.env['product.product'].search([('product_tmpl_id','=',self.id)])
        if product_ids:
            for product_id in product_ids:
                product_id.action_countinued()
                
        self.is_discountinued = False
    
            
    
    is_discountinued = fields.Boolean('Is Discontinued?')
    
    
    
    

class ProductProduct(models.Model):
    _inherit = 'product.product'   
    
    
    def action_discountinued(self):
        self.is_discountinued = True
    
    def action_countinued(self):
        self.is_discountinued = False
    
    def compute_expected_date(self):
        StockPicking = self.env['stock.picking']
        StockMove = self.env['stock.move']
        
        for rec in self:
            move_ids = StockMove.search([('product_id','=',rec.id),('picking_id','!=',False),
                                            ('picking_id.purchase_id','!=',False),('state','=','assigned')])
            
            if move_ids:
                picking_id =  StockPicking.search([('id','in',move_ids.picking_id.ids)], order="scheduled_date asc", limit=1)
                
                if picking_id:
                    rec.expected_date_receving = picking_id.scheduled_date
                else:
                    rec.expected_date_receving = None
            else:
                rec.expected_date_receving = None
            
    
    def compute_all_lot_ids(self):
        for rec in self:
            rec.all_lot_ids = rec.stock_quant_ids.lot_id.ids       
            
            
    
    expected_date_receving = fields.Datetime(string='Expected Date', compute='compute_expected_date')
    is_discountinued = fields.Boolean('Is Discontinued?')
    all_lot_ids = fields.Many2many('stock.production.lot', compute='compute_all_lot_ids')
    
    