# -*- coding: utf-8 -*-

from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    customer = fields.Boolean(string='Es cliente')
    supplier = fields.Boolean(string='Es proveedor')

