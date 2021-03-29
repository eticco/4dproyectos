# -*- coding: utf-8 -*-
from odoo import models, fields, api

class ProductProduct(models.Model):
    _inherit = 'product.product'
    
    workorders_count = fields.Integer(string="Órdenes de trabajo", compute="_compute_workorders_count")


    def _compute_workorders_count(self):
        for product_id in self:
            if isinstance(product_id.id, int):
                product_id.workorders_count = self.env['mrp.workorder'].search_count([('product_id.id', '=', product_id.id)])
            else:
                product_id.workorders_count = 0

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    workorders_count = fields.Integer(string="Órdenes de trabajo", compute="_compute_workorders_count")


    def _compute_workorders_count(self):
        for product_tmpl_id in self:
            if isinstance(product_tmpl_id.id, int):
                product_tmpl_id.workorders_count = self.env['mrp.workorder'].search_count([('product_tmpl_id.id', '=', product_tmpl_id.id)])
            else:
                product_tmpl_id.workorders_count = 0
