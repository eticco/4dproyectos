# -*- coding: utf-8 -*-
from odoo import models, fields


class HrJob(models.Model):
    _inherit = 'hr.job'
    
    timesheet_cost = fields.Monetary('Timesheet Cost', currency_field='currency_id',
        groups="hr.group_hr_user", default=0.0)
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id', readonly=True)
