# # -*- coding: utf-8 -*-
from . import config
from . import update
from collections import defaultdict
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models, _
from odoo.osv import expression
from odoo.exceptions import UserError
from collections import OrderedDict
from operator import itemgetter
from datetime import datetime , date
from odoo import http, _
from odoo.exceptions import AccessError, MissingError
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo.tools import groupby as groupbyelem
from odoo.osv.expression import OR
from datetime import date, datetime, timedelta
from odoo import exceptions
from dateutil.relativedelta import relativedelta
import base64
import binascii

def request_page_content(flag = 0):
    products = request.env['product.product'].search([])
    company_info = request.env['res.users'].search([('id','=',http.request.env.context.get('uid'))])
    return {
        'products' : products,
        'success_flag' : flag,
        'company_info' : company_info
    }
   


def paging(data, flag1 = 0, flag2 = 0):        
    if flag1 == 1:
        return config.list12
    elif flag2 == 1:
        config.list12.clear()
    else:
        k = []
        for rec in data:
            for ids in rec:
                config.list12.append(ids.id)        
 
    
        
class CreateRequest(http.Controller):

    @http.route('/request/create/',type="http", website=True, auth='user')
    def request_create_template(self, **kw):
        return request.render("de_misc_request_portal.request_template",request_page_content()) 
    
    @http.route('/my/request/save', type="http", auth="public", website=True)
    def request_submit_forms(self, **kw):
        if kw.get('description'):
            request_val = {
                'employee_id': int(kw.get('employee_id')),            
                'request_type_id':kw.get('request_type_id'),
                'description': kw.get('description'),
                'best_before_date': kw.get('best_before_date'),
            }
            record = request.env['hr.request'].sudo().create(request_val)
            record.action_submit()
            
        return request.render("de_misc_request_portal.request_submitted", {}, request_page_content())
  

    
    
    
class CustomerPortal(CustomerPortal):

    

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if 'product_count' in counters:
            values['product_count'] = request.env['product.product'].search_count([])
        return values
  
    def _request_get_page_view_values(self,product_id, next_id = 0,pre_id= 0, request_user_flag = 0, access_token = None, **kwargs):
        company_info = request.env['res.users'].search([('id','=',http.request.env.context.get('uid'))])
        values = {
            'page_name': 'request',
            'product_id': product_id,
            'request_user_flag':request_user_flag,
            'next_id' : next_id,
            'company_info': company_info,
            'pre_id' : pre_id,
        }
        return self._get_page_view_values(product_id, access_token, values, 'my_product_history', False, **kwargs)
    

    @http.route(['/my/products', '/my/products/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_products(self, page=1, date_begin=None, date_end=None, sortby=None, filterby=None, search=None, search_in='content', groupby=None, **kw):
        
        values = self._prepare_portal_layout_values()
        searchbar_sortings = {
            'date': {'label': _('Newest'), 'order': 'create_date desc'},
            'categ_id': {'label': _('Category'), 'order': 'categ_id desc' },
            'update': {'label': _('Last Update'), 'order': 'write_date desc'},
        }
        
        searchbar_filters = {
            'all': {'label': _('All'), 'domain': [('type', 'in', ['consu', 'service','product'])]},
            
            'consu': {'label': _('Consumable'), 'domain': [('type', '=', 'consu')]},
            'service': {'label': _('Service'), 'domain': [('type', '=', 'service')]},  
            'product': {'label': _('Storeable'), 'domain': [('type', '=', 'product')]},
        }
                                 
        
        searchbar_inputs = { 
            'content': {'input': 'content', 'label': _('Search <span class="nolabel"> (in Content)</span>')}, 
            'name': {'input': 'name', 'label': _('Search in Product')},
            'default_code': {'input': 'default_code', 'label': _('Search in Ref#')},
#             'all': {'input': 'all', 'label': _('Search in All')},
        }
        searchbar_groupby = {
            'none': {'input': 'none', 'label': _('None')},
        }

        request_groups = request.env['product.product'].search([])

        # default sort by value
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']

        # default filter by value
        if not filterby:
            filterby = 'all'
        domain = searchbar_filters.get(filterby, searchbar_filters.get('all'))['domain']
        if date_begin and date_end:
            domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]       

        # search
        if search and search_in:
            search_domain = []
            if search_in in ('content'):
                search_domain = OR([search_domain, [('default_code', 'ilike', search)]])
            if search_in in ('name', 'default_code'):
                search_domain = OR([search_domain, [('name', 'ilike', search)]])
            if search_in in ('name', 'default_code'):
                search_domain = OR([search_domain, [('default_code', 'ilike', search)]])
            domain += search_domain
        product_count = request.env['product.product'].search_count(domain)

        # pager
        pager = portal_pager(
            url="/my/products",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby, 'filterby': filterby,
                      'seissuesarch_in': search_in, 'search': search},
            total=555,
            page=page,
            step=self._items_per_page
        )

        _product = request.env['product.product'].search(domain, order=order, limit=self._items_per_page, offset=pager['offset'])
        request.session['my_product_history'] = _product.ids[:100]

        grouped_products = [_product]
                
        paging(0,0,1)
        paging(grouped_products)
        company_info = request.env['res.users'].search([('id','=',http.request.env.context.get('uid'))])
        values.update({
            'date': date_begin,
            'date_end': date_end,
            'grouped_products': grouped_products,
            'page_name': 'Products',
            'default_url': '/my/products',
            'pager': pager,
            'company_info': company_info,
            'searchbar_sortings': searchbar_sortings,
            'searchbar_inputs': searchbar_inputs,
            'search_in': search_in,
            'search': search,
            'sortby': sortby,
            'groupby': groupby,
            'searchbar_filters': OrderedDict(sorted(searchbar_filters.items())),
        })
        return request.render("aces_product_inventory_portal.portal_my_products", values)

   
    @http.route(['/my/product/<int:product_id>'], type='http', auth="user", website=True)
    def portal_my_product(self, product_id, access_token=None, **kw):
        try:
            product_sudo = self._document_check_access('product.product', product_id, access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')
        
        print('product_sudo',product_sudo)

        next_id = 0
        pre_id = 0
        request_user_flag = 0
                 
        product_id_list = paging(0,1,0)
        next_next_id = 0
        product_id_list.sort()
        length_list = len(product_id_list)
        length_list = length_list - 1
        if length_list != 0:
            if product_id in product_id_list:
                product_id_loc = product_id_list.index(product_id)
                if product_id_loc == 0:
                    next_id = 1
                    pre_id = 0
                elif product_id_loc == length_list:
                    next_id = 0
                    pre_id = 1
                else:
                    next_id = 1
                    pre_id = 1
        else:
            next_id = 0
            pre_id = 0
 
 
        values = self._request_get_page_view_values(product_sudo,next_id, pre_id,access_token, **kw) 
        return request.render("aces_product_inventory_portal.portal_my_product", values)
    
    
        
    
    @http.route(['/product/next/<int:product_id>'], type='http', auth="user", website=True)
    def portal_my_next_request(self, product_id, access_token=None, **kw):
         
        product_id_list = paging(0,1,0)
        next_next_id = 0
        product_id_list.sort()
         
        length_list = len(product_id_list)
        if length_list == 0:
            return request.redirect('/my')
        length_list = length_list - 1
         
        if product_id in product_id_list:
            product_id_loc = product_id_list.index(product_id)
            next_next_id = product_id_list[product_id_loc + 1] 
            next_next_id_loc = product_id_list.index(next_next_id)
            if next_next_id_loc == length_list:
                next_id = 0
                pre_id = 1
            else:
                next_id = 1
                pre_id = 1      
        else:
            buffer_larger = 0
            buffer_smaller = 0
            buffer = 0
            for ids in product_id_list:
                if ids < timeoff_id:
                    buffer_smaller = ids
                if ids > timeoff_id:
                    buffer_smaller = ids
                if buffer_larger and buffer_smaller:
                    break
            if buffer_larger:
                next_next_id = buffer_smaller
            elif buffer_smaller:
                next_next_id = buffer_larger
                 
            next_next_id_loc = product_id_list.index(next_next_id)
            length_list = len(product_id_list)
            length_list = length_list + 1
            if next_next_id_loc == length_list:
                next_id = 0
                pre_id = 1
            elif next_next_id_loc == 0:
                next_id = 1
                pre_id = 0
            else:
                next_id = 1
                pre_id = 1
          
        values = []
        active_user = http.request.env.context.get('uid')
        id = product_id
        try:
            request_sudo = self._document_check_access('product.product', next_next_id, access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')
         
 
        values = self._request_get_page_view_values(request_sudo,next_id, pre_id, access_token, **kw) 
        return request.render("aces_product_inventory_portal.portal_my_product", values)
 
   
    @http.route(['/product/pre/<int:product_id>'], type='http', auth="user", website=True)
    def portal_my_pre_request(self, product_id, access_token=None, **kw):
         
        product_id_list = paging(0,1,0)
        pre_pre_id = 0
        product_id_list.sort()
        length_list = len(product_id_list)
     
        if length_list == 0:
            return request.redirect('/my')
         
        length_list = length_list - 1
        if product_id in product_id_list:
            product_id_loc = product_id_list.index(product_id)
            pre_pre_id = product_id_list[product_id_loc - 1] 
            pre_pre_id_loc = product_id_list.index(product_id)
 
            if product_id_loc == 1:
                next_id = 1
                pre_id = 0
            else:
                next_id = 1
                pre_id = 1      
        else:
            buffer_larger = 0
            buffer_smaller = 0
            buffer = 0
            for ids in product_id_list:
                if ids < product_id:
                    buffer_smaller = ids
                if ids > product_id:
                    buffer_smaller = ids
                if buffer_larger and buffer_smaller:
                    break
            if buffer_smaller:
                pre_pre_id = buffer_smaller
            elif buffer_larger:
                pre_pre_id = buffer_larger
                 
            pre_pre_id_loc = product_id_list.index(pre_pre_id)
            length_list = len(product_id_list)
            length_list = length_list -1
            if pre_pre_id_loc == 0:
                next_id = 1
                pre_id = 0
            elif pre_pre_id_loc == length_list:
                next_id = 0
                pre_id = 1
            else:
                next_id = 1
                pre_id = 1
    
        values = []
 
        id = pre_pre_id
        try:
            product_sudo = self._document_check_access('product.product', pre_pre_id, access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')
         
        product_user_flag = 0
 
 
        values = self._request_get_page_view_values(product_sudo, next_id,pre_id, access_token, **kw) 
        return request.render("aces_product_inventory_portal.portal_my_product", values)
