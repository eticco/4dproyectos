# -*- coding: utf-8 -*-
from odoo import models, fields, api


class MrpWorkorder(models.Model):
    _inherit = 'mrp.workorder'
    
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id', readonly=True)    
    workcenter_cost = fields.Monetary(string='Coste maquinaria', currency_field='currency_id', compute='_compute_workcenter_cost')
    users_cost = fields.Monetary(string='Coste mano obra', currency_field='currency_id', compute='_compute_users_cost')

    duration_per_unit = fields.Float(string='Duración/unidad', compute='_compute_per_unit')
    workcenter_cost_per_unit =fields.Monetary(string='Coste maquinaria unitario', currency_field='currency_id', compute='_compute_per_unit')
    users_cost_per_unit = fields.Monetary(string='Coste mano obra unitario', currency_field='currency_id', compute='_compute_per_unit')

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
            criteria_found = False
            for criteria_id in order.production_id.criteria_amount_ids:
                if criteria_id.computation_criteria_id.id == order.workcenter_id.computation_criteria_id.id:
                    criteria_found = True
                    if criteria_id.amount > 0:
                        order.duration_per_unit = order.duration / criteria_id.amount
                        order.workcenter_cost_per_unit = order.workcenter_cost / criteria_id.amount
                        order.users_cost_per_unit = order.users_cost / criteria_id.amount
                    else:
                        order.duration_per_unit = 0.0
                        order.workcenter_cost_per_unit = 0.0
                        order.users_cost_per_unit = 0.0
                    break
            if not criteria_found:
                order.duration_per_unit = 0.0
                order.workcenter_cost_per_unit = 0.0
                order.users_cost_per_unit = 0.0
                
