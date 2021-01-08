# -*- coding: utf-8 -*-
from odoo import models, fields, api


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'
    
    production_id = fields.Many2one(comodel_name="mrp.production", string="Orden de producción")
    
    