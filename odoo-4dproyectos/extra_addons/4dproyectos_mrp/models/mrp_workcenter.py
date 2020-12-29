# -*- coding: utf-8 -*-
from odoo import models, fields, api


class MrpWorkcenter(models.Model):
    _inherit = 'mrp.workcenter'
    
    computation_criteria_id = fields.Many2one(string="Criterio de cómputo", comodel_name="mrp.computation.criteria")


class MrpWorkcenterProductivity(models.Model):
    _inherit = "mrp.workcenter.productivity"
    
    user_cost = fields.Float(string='Coste/empleado', compute='_compute_user_cost')
    
    @api.depends('duration', 'user_id')
    def _compute_user_cost(self):
        for line in self:
            employee_id = self.env['hr.employee'].search([('user_id', '=', line.user_id.id)], limit=1)
            line.user_cost = line.duration * employee_id.timesheet_cost / 60.0
    