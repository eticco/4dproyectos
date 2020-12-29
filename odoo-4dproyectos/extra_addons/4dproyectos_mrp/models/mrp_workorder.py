# -*- coding: utf-8 -*-
from odoo import models, fields, api


class MrpWorkorder(models.Model):
    _inherit = 'mrp.workorder'
    
    workcenter_cost = fields.Float(string='Coste/máquina', compute='_compute_workcenter_cost')
    users_cost = fields.Float(string='Coste/empleados', compute='_compute_users_cost')

    @api.depends('duration', 'workcenter_id')
    def _compute_workcenter_cost(self):
        for order in self:
            order.workcenter_cost = order.duration * order.workcenter_id.costs_hour

    @api.depends('time_ids.user_cost')
    def _compute_users_cost(self):
        for order in self:
            order.users_cost = sum(order.time_ids.mapped('user_cost'))

