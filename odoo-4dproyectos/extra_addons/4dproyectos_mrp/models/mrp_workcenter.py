# -*- coding: utf-8 -*-
from odoo import models, fields, api


class MrpWorkcenter(models.Model):
    _inherit = 'mrp.workcenter'
    
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id', readonly=True)    
    computation_criteria_id = fields.Many2one(string="Criterio de cómputo", comodel_name="mrp.computation.criteria")
    duration_expected_per_unit = fields.Float(string="Duración esperada/unidad", help="En minutos. Por ejemplo, 52:30 representan 52 minutos y 30 segundos")
    costs_hour_users = fields.Monetary(string='Coste estimado mano obra por hora', currency_field='currency_id', help="Se utiliza para calcular el coste estimado de mano obra en este puesto")

class MrpWorkcenterProductivity(models.Model):
    _inherit = "mrp.workcenter.productivity"
    
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id', readonly=True)    
    user_cost = fields.Monetary(string='Coste', currency_field='currency_id', compute='_compute_user_cost')
    
    @api.depends('duration', 'user_id')
    def _compute_user_cost(self):
        for line in self:
            employee_id = self.env['hr.employee'].search([('user_id', '=', line.user_id.id)], limit=1)
            line.user_cost = line.duration * employee_id.timesheet_cost / 60.0

class MrpRoutingWorkcenter(models.Model):
    _inherit = "mrp.routing.workcenter"
    
    duration_expected_per_unit = fields.Float(string="Duración esperada/unidad", related='workcenter_id.duration_expected_per_unit', readonly=True, help="En minutos. Por ejemplo, 52:30 representan 52 minutos y 30 segundos")