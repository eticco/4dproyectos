# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.osv import expression


class MrpWorkorder(models.Model):
    _inherit = 'mrp.workorder'
    
    workcenter_name = fields.Char(string='Nombre centro producción', related='workcenter_id.name', store=True)

    currency_id = fields.Many2one('res.currency', related='company_id.currency_id', readonly=True)
    project_id = fields.Many2one('project.project', related='production_id.project_id', readonly=True)
    product_id = fields.Many2one('product.product', related='production_id.product_id', readonly=True) 
    product_tmpl_id = fields.Many2one('product.template', related='production_id.product_id.product_tmpl_id', readonly=True) 
    workcenter_cost = fields.Monetary(string='Coste maquinaria', currency_field='currency_id', compute='_compute_workcenter_cost')
    users_cost = fields.Monetary(string='Coste mano obra', currency_field='currency_id', compute='_compute_users_cost')

    duration_per_unit = fields.Float(string='Duración/unidad', compute='_compute_per_unit', help="Tiempo real por unidad. Es el resultado de dividir el tiempo total entre las unidades")
    workcenter_cost_per_unit =fields.Monetary(string='Coste maquinaria unitario', currency_field='currency_id', compute='_compute_per_unit')
    users_cost_per_unit = fields.Monetary(string='Coste mano obra unitario', currency_field='currency_id', compute='_compute_per_unit')
    real_total_cost = fields.Monetary(string='Coste real total', currency_field='currency_id', compute='_compute_real_total_cost', help="Coste total real. Es la suma de los costes reales de mano de obra y maquinaria")
    real_total_cost_per_unit = fields.Monetary(string='Coste real total unitario', currency_field='currency_id', compute='_compute_per_unit', help="Coste real/unidad. Es el resultado de dividir el coste total real entre las unidades")

    # Este dato nos lo tienen que facilitar en el centro de producción y se hereda aquí
    duration_expected_per_unit = fields.Float(string='Duración esperada/unidad', related='workcenter_id.duration_expected_per_unit', readonly=True, help="Tiempo estimado por unidad. Fijado en el puesto de producción")
    # La duración esperada total es igual a la duració unitaria por el número de unidades de cómputo
    duration_expected_4d = fields.Float(string='Duración esperada total',  compute='_compute_duration_expected_4d', readonly=True, help="Tiempo estimado total, multiplicando el tipo estimado por unidad por el número de piezas a trabajar en el puesto")
    # Es el coste maquinaria por hora del centro de producción multiplicado por el tiempo esperado de cada unidad por el número de unidades
    estimated_workcenter_cost = fields.Monetary(string='Coste estimado maquinaria', currency_field='currency_id', compute='_compute_estimated_workcenter_cost', help="Es el coste maquinaria por hora del centro de producción multiplicado por el tiempo esperado de cada unidad por el número de unidades")
    # Es el coste mano obra por hora del centro de producción multiplicado por el tiempo esperado de cada unidad por el número de unidades
    estimated_users_cost = fields.Monetary(string='Coste estimado mano obra', currency_field='currency_id', compute='_compute_estimated_users_cost', help="Es el coste mano obra por hora del centro de producción multiplicado por el tiempo esperado de cada unidad por el número de unidades")
    # Es la suma del coste estimado de maquinaria más el coste estimado de mano de obra
    estimated_total_cost = fields.Monetary(string='Coste estimado total', currency_field='currency_id', compute='_compute_estimated_total_cost', help="Coste estimado total. Es la suma del coste estimado de maquinaria más el coste estimado de mano de obra")
    # Es el resultado de dividir el coste estimado total entre las unidades
    estimated_total_cost_per_unit = fields.Monetary(string='Coste estimado/unitario', currency_field='currency_id', compute='_compute_estimated_total_cost_per_unit', help="Coste estimado por unidad. Es el resultado de dividir el coste estimado total entre las unidades")

    
    # Guarda la fila de las cantidades de cómputo de la orden de producción que aplica a esta orden de trabajo
    criteria_amount_id = fields.Many2one(comodel_name = 'mrp.production.criteria.amount', string = 'Criterio de cómputo', compute='_compute_criteria_amount_id')
    criteria_name = fields.Char(string='Criterio de cómputo', related='criteria_amount_id.computation_criteria_id.name')
    criteria_amount = fields.Integer(string='Cantidad', related='criteria_amount_id.amount')


    def name_get(self):
        result = []
        for rec in self:
            result.append((rec.id, rec.workcenter_id.name))
        return result            

    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        domain = []
        if name:
            domain = [('workcenter_name', operator, name)]
        return self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)

    @api.depends('production_id', 'workcenter_id')
    def _compute_criteria_amount_id(self):
        for order in self:
            criteria_amount_id = None
            for criteria_id in order.production_id.criteria_amount_ids:
                if criteria_id.computation_criteria_id.id == order.workcenter_id.computation_criteria_id.id:
                    criteria_amount_id = criteria_id
                    break
            order.criteria_amount_id = criteria_amount_id

    @api.depends('duration', 'workcenter_id')
    def _compute_workcenter_cost(self):
        for order in self:
            order.workcenter_cost = order.duration * order.workcenter_id.costs_hour / 60.0

    @api.depends('time_ids.user_cost')
    def _compute_users_cost(self):
        for order in self:
            order.users_cost = sum(order.time_ids.mapped('user_cost'))

    @api.depends('workcenter_cost','users_cost')
    def _compute_real_total_cost(self):
        for order in self:
            order.real_total_cost = order.workcenter_cost + order.users_cost

    @api.depends('criteria_amount_id','duration_expected_per_unit')
    def _compute_duration_expected_4d(self):
        for order in self:
            order.duration_expected_4d = order.criteria_amount_id.amount * order.duration_expected_per_unit

    @api.depends('duration_expected_per_unit','criteria_amount_id','workcenter_id')
    def _compute_estimated_workcenter_cost(self):
        for order in self:
            order.estimated_workcenter_cost = order.duration_expected_per_unit * order.criteria_amount_id.amount * order.workcenter_id.costs_hour / 60.0

    @api.depends('duration_expected_per_unit','criteria_amount_id','workcenter_id')
    def _compute_estimated_users_cost(self):
        for order in self:
            order.estimated_users_cost = order.duration_expected_per_unit * order.criteria_amount_id.amount * order.workcenter_id.costs_hour_users / 60.0

    @api.depends('estimated_workcenter_cost', 'estimated_users_cost')
    def _compute_estimated_total_cost(self):
        for order in self:
            order.estimated_total_cost = order.estimated_workcenter_cost + order.estimated_users_cost 

    @api.depends('estimated_total_cost', 'criteria_amount_id')
    def _compute_estimated_total_cost_per_unit(self):
        for order in self:
            if order.criteria_amount_id.amount > 0:
                order.estimated_total_cost_per_unit = order.estimated_total_cost / order.criteria_amount_id.amount
            else:
                order.estimated_total_cost_per_unit = 0.0

    @api.depends('duration', 'workcenter_cost', 'users_cost', 'real_total_cost', 'criteria_amount_id')
    def _compute_per_unit(self):
        for order in self:
            if order.criteria_amount_id.amount > 0:
                order.duration_per_unit = order.duration / order.criteria_amount_id.amount
                order.workcenter_cost_per_unit = order.workcenter_cost / order.criteria_amount_id.amount
                order.users_cost_per_unit = order.users_cost / order.criteria_amount_id.amount
                order.real_total_cost_per_unit = order.real_total_cost / order.criteria_amount_id.amount
            else:
                order.duration_per_unit = 0.0
                order.workcenter_cost_per_unit = 0.0
                order.users_cost_per_unit = 0.0
                order.real_total_cost_per_unit = 0.0
                
