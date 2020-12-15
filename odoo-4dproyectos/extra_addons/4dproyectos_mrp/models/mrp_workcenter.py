# -*- coding: utf-8 -*-
from odoo import models, fields, api


class MrpWorkcenter(models.Model):
    _inherit = 'mrp.workcenter'
    
    computation_criteria_id = fields.Many2one(string="Criterio de cómputo", comodel_name="mrp.computation.criteria")
