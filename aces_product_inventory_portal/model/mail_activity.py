# -*- coding: utf-8 -*-
from odoo import api, fields, models, _




class ProductCategory(models.Model):
    _inherit = 'product.category'
    
    
class StockPicking(models.Model):
    _inherit = 'stock.picking'
    

class UomUom(models.Model):
    _inherit = 'uom.uom'
    
    
class StockQuant(models.Model):
    _inherit = 'stock.quant'
    

class StockMove(models.Model):
    _inherit = 'stock.move' 

class StockLocation(models.Model):
    _inherit = 'stock.location' 


class StockWarehouse(models.Model):
    _inherit = 'stock.warehouse' 
    
    
class ProductTemplate(models.Model):
    _inherit = 'product.template'  

class MailActivity(models.Model):
    _inherit = 'mail.activity'   
    