# -*- coding: utf-8 -*-
from odoo import models, fields, api


class MrpProduction(models.Model):
    _inherit = 'mrp.production'
    
    code = fields.Char('Código', readonly=True)
    criteria_amount_ids = fields.One2many(comodel_name = 'mrp.production.criteria.amount', inverse_name = 'production_id', string = 'Cantidades de cómputo', ondelete="cascade")
    partner_id = fields.Many2one(comodel_name="res.partner", string="Cliente", required=True)
    project_id = fields.Many2one(comodel_name="project.project", string="Proyecto", required=True)
    price = fields.Monetary(string='Precio de venta', currency_field='currency_id')
    notes = fields.Text('Notes')
    date_start = fields.Datetime('Start Date', readonly=False)
    date_finished = fields.Datetime('End Date', readonly=False)
    wood_id = fields.Many2one(comodel_name="mrp.wood", string="Madera") 
    varnish_id = fields.Many2one(comodel_name="mrp.varnish", string="Barniz")
    aluminum_color_id = fields.Many2one(comodel_name="mrp.aluminum.color", string="Color aluminio") 
    glass = fields.Boolean('Vidrio')
    blind = fields.Boolean('Persiana')
    boards = fields.Integer("Tableros")
    type = fields.Selection(string="Tipo", selection=[('sin_colocacion','Sin colocación'), ('colocacion_obra_nueva','Colocación obra nueva'), ('colocacion_obra_reforma','Colocación obra reforma')])

    currency_id = fields.Many2one('res.currency', related='company_id.currency_id', readonly=True)

    wood_cost = fields.Monetary(string="Coste madera", currency_field='currency_id')
    glass_cost = fields.Monetary(string="Coste vidrio", currency_field='currency_id')
    ironwork_cost = fields.Monetary(string="Coste herrajes", currency_field='currency_id')
    blind_cost = fields.Monetary(string="Coste persianas")
    aluminum_cost = fields.Monetary(string="Coste aluminio", currency_field='currency_id')
    other_cost = fields.Monetary(string="Coste varios", currency_field='currency_id')
    raw_material_cost = fields.Monetary(string="Coste total materiales", currency_field='currency_id', compute='_compute_raw_material_cost')
    users_cost = fields.Monetary(string="Coste total mano obra", currency_field='currency_id', compute='_compute_users_cost')
    workcenters_cost = fields.Monetary(string="Coste total máquinas", currency_field='currency_id', compute='_compute_workcenters_cost')
    
    @api.depends('wood_cost','glass_cost','ironwork_cost','blind_cost','aluminum_cost','other_cost')
    def _compute_raw_material_cost(self):
        
        for production in self:
            production.raw_material_cost = production.wood_cost + production.glass_cost + production.ironwork_cost + production.blind_cost + production.aluminum_cost + production.other_cost
    
    def _compute_users_cost(self):
        
        for production in self:
            production.users_cost = sum(production.workorder_ids.mapped('users_cost'))
    
    def _compute_workcenters_cost(self):
        
        for production in self:
            production.workcenters_cost = sum(production.workorder_ids.mapped('workcenter_cost'))
            
            
    @api.model
    def create(self, values):
        code = 'Autogenerado'
        values['code'] = code
        result = super(MrpProduction, self).create(values)

        computation_criterias = self.env['mrp.computation.criteria'].search([])
        for cc in computation_criterias:
            self.env['mrp.production.criteria.amount'].create({
                'computation_criteria_id': cc.id,
                'production_id': result.id,
            })
        
        return result

class MrpProductionCriteriaAmount(models.Model):
    _name = 'mrp.production.criteria.amount'

    computation_criteria_id = fields.Many2one(comodel_name="mrp.computation.criteria", string="Criterio de cómputo", required=True, readonly=True)
    production_id = fields.Many2one(comodel_name="mrp.production", string="Orden de producción", required=True, readonly=True)
    amount = fields.Integer(string="Cantidad")


class MrpWood(models.Model):
    _name = 'mrp.wood'
    
    name = fields.Char('Nombre')

class MrpVarnish(models.Model):
    _name = 'mrp.varnish'
    
    name = fields.Char('Nombre')

class MrpAluminumColor(models.Model):
    _name = 'mrp.aluminum.color'
    
    name = fields.Char('Nombre')
