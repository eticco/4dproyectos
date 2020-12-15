# -*- coding: utf-8 -*-
from odoo import models, fields, api


class MrpComputationCriteria(models.Model):
    
    _name = 'mrp.computation.criteria'

    name = fields.Char(string = 'Nombre', required = True)
