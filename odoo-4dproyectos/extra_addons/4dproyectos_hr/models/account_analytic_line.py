# -*- coding: utf-8 -*-
from odoo import models, fields


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'
    
    production_id = fields.Many2one(comodel_name="mrp.production", string="Orden de producción")
    workorder_id = fields.Many2one(comodel_name="mrp.workorder", string="Orden de trabajo")
