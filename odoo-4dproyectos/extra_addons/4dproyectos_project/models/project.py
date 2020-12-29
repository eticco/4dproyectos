# -*- coding: utf-8 -*-

from odoo import api, models, fields
import logging
_logger = logging.getLogger(__name__)

class Project(models.Model):
    _inherit = 'project.project'

    partner_shipping_id = fields.Many2one('res.partner', string='Dirección')
    production_ids = fields.One2many(comodel_name = 'mrp.production', inverse_name = 'project_id', string = 'Órdenes de producción')
    total_budget = fields.Float(string="Presupuesto total", currency_field='currency_id')
    raw_material_cost = fields.Monetary(string="Coste total materiales", currency_field='currency_id', compute='_compute_raw_material_cost', help='Obtenido como la suma de los costes de materiales de sus órdenes de producción')
    users_cost = fields.Monetary(string="Coste total mano obra", currency_field='currency_id', compute='_compute_users_cost', help='Obtenido como la suma de los costes de mano de obra de sus órdenes de producción')
    workcenters_cost = fields.Monetary(string="Coste total maquinaria", currency_field='currency_id', compute='_compute_workcenters_cost', help='Obtenido como la suma de los costes de maquinaria de sus órdenes de producción')
    status = fields.Selection(string="Estado", selection=[('contratada', 'Contratada'), ('en_ejecucion', 'En ejecución'), ('terminada_en_fabrica', 'Terminada en fábrica'), ('entregada', 'Entregada'), ('facturada', 'Facturada'), ('cerrada', 'Cerrada')])
    start_date = fields.Date(string="Fecha de alta")

    
    def _compute_raw_material_cost(self):
        
        for project in self:
            project.raw_material_cost = sum(project.production_ids.mapped('raw_material_cost'))
    
    def _compute_users_cost(self):
        
        for project in self:
            project.users_cost = sum(project.production_ids.mapped('users_cost'))
    
    def _compute_workcenters_cost(self):
        
        for project in self:
            project.workcenters_cost = sum(project.production_ids.mapped('workcenters_cost'))
