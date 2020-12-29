# -*- coding: utf-8 -*-
from odoo import models, fields, api


class MrpWorkorder(models.Model):
    _inherit = 'mrp.workorder'
    
    workcenter_cost = fields.Float(string='Coste/máquina', compute='_compute_workcenter_cost')
    users_cost = fields.Float(string='Coste/empleados', compute='_compute_users_cost')
    
    duration_per_unit = fields.Float(string='Duración/unidad', compute='_compute_per_unit')
    workcenter_cost_per_unit =fields.Float(string='Coste/máquina unitario', compute='_compute_per_unit')
    users_cost_per_unit = fields.Float(string='Coste/empleados unitario', compute='_compute_per_unit')

    @api.depends('duration', 'workcenter_id')
    def _compute_workcenter_cost(self):
        for order in self:
            order.workcenter_cost = order.duration * order.workcenter_id.costs_hour / 60.0

    @api.depends('time_ids.user_cost')
    def _compute_users_cost(self):
        for order in self:
            order.users_cost = sum(order.time_ids.mapped('user_cost'))

    @api.depends('duration')
    def _compute_per_unit(self):
        for order in self:
            for criteria_id in order.production_id.criteria_amount_ids:
                if criteria_id.computation_criteria_id.id == order.workcenter_id.computation_criteria_id.id:
                    if criteria_id.amount > 0:
                        order.duration_per_unit = order.duration / criteria_id.amount
                        order.workcenter_cost_per_unit = order.workcenter_cost / criteria_id.amount
                        order.users_cost_per_unit = order.users_cost / criteria_id.amount
                    else:
                        order.duration_per_unit = 0.0
                        order.workcenter_cost_per_unit = 0.0
                        order.users_cost_per_unit = 0.0
                    break

