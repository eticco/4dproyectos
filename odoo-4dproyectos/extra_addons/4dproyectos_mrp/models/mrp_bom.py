# -*- coding: utf-8 -*-
from odoo import models, fields, api


class MrpBom(models.Model):
    _inherit = 'mrp.bom'
    
    is_default_pricelist = fields.Boolean('Por defecto', default=False)