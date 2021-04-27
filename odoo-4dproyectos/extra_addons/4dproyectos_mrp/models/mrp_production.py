# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import datetime
import logging
_logger = logging.getLogger(__name__)

class MrpProduction(models.Model):
    _inherit = 'mrp.production'
    
    code = fields.Char('Código', readonly=True)
    product_qty = fields.Float(string='Nº unidades')
    sheet_qty = fields.Integer(string='Nº hojas', compute='_compute_sheet_qty')
    criteria_amount_ids = fields.One2many(comodel_name = 'mrp.production.criteria.amount', inverse_name = 'production_id', string = 'Cantidades de cómputo', ondelete="cascade")
    partner_id = fields.Many2one(comodel_name="res.partner", string="Cliente", required=True)
    project_id = fields.Many2one(comodel_name="project.project", string="Obra", required=True)
    internal_by_project_id = fields.Integer(string="Numeración de OF dentro de la misma obra")
    price = fields.Monetary(string='Precio de venta', currency_field='currency_id')
    notes = fields.Text('Notes')
    date_start = fields.Datetime('Start Date', related='create_date')
    date_loaded = fields.Datetime('Fecha carga', readonly=True)
    wood_id = fields.Many2one(comodel_name="mrp.wood", string="Madera") 
    varnish_id = fields.Many2one(comodel_name="mrp.varnish", string="Barniz")
    aluminum_color_id = fields.Many2one(comodel_name="mrp.aluminum.color", string="Color aluminio") 
    glass = fields.Boolean('Vidrio')
    blind = fields.Boolean('Persiana')
    boards = fields.Integer("Tableros")
    type = fields.Selection(string="Tipo", selection=[('sin_colocacion','Sin colocación'), ('colocacion_obra_nueva','Colocación obra nueva'), ('colocacion_obra_reforma','Colocación obra reforma')])
    custom_state = fields.Selection(selection=[('draft','Borrador'), ('progress','En progreso'), ('done','Hecho'), ('loaded','Cargado '), ('cancel','Cancelado')], readonly=False, string='Estado',
        copy=False, index=True,
        store=True, tracking=True)
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id', readonly=True)

    wood_cost = fields.Monetary(string="Coste madera", currency_field='currency_id')
    glass_cost = fields.Monetary(string="Coste vidrio", currency_field='currency_id')
    ironwork_cost = fields.Monetary(string="Coste herrajes", currency_field='currency_id')
    blind_cost = fields.Monetary(string="Coste persianas")
    aluminum_cost = fields.Monetary(string="Coste aluminio", currency_field='currency_id')
    other_cost = fields.Monetary(string="Coste varios", currency_field='currency_id')
    raw_material_cost = fields.Monetary(string="Coste total materiales", currency_field='currency_id', compute='_compute_raw_material_cost', help='Obtenido como la suma de los costes de madera, vidrio, etc.')
    varnish_cost = fields.Monetary(string="Coste barniz", currency_field='currency_id')
    users_cost = fields.Monetary(string="Coste total mano obra", currency_field='currency_id', compute='_compute_users_cost', help='Obtenido como la suma de los costes de mano de obra de todos los puestos de producción')
    workcenters_cost = fields.Monetary(string="Coste total maquinaria", currency_field='currency_id', compute='_compute_workcenters_cost', help='Obtenido como la suma de los costes de maquinaria de todos los puestos de producción')
    real_total_cost_per_unit = fields.Monetary(string="Coste real total por unidad", currency_field='currency_id', compute='_compute_real_total_cost_per_unit', help='Obtenido como la suma de los costes de mano de obra y maquinaria por unidad')
    real_total_cost = fields.Monetary(string="Coste real total mano obra y maquinaria", currency_field='currency_id', compute='_compute_real_total_cost', help='Obtenido como la suma de los costes de mano de obra y maquinaria')
    packaging_cost = fields.Monetary(string="Coste embalaje, carga y descarga", currency_field='currency_id', help="Sólo rellenar este campo en la órdenes de fabricación de ventanas, multiplicando el coste medio anual por el número de ventanas")
    varnish_ids = fields.One2many(comodel_name = 'mrp.varnish', inverse_name = 'production_id', string = 'Barnices')

    def name_get(self):
        result = []
        for rec in self:
            result.append((rec.id, rec.code))
        return result            

    def _compute_sheet_qty(self):
        
        for production in self:
            production.sheet_qty = 0
            for criteria_amount_id in production.criteria_amount_ids:
                if "Nº de hojas de ventana" == criteria_amount_id.computation_criteria_id.name:
                    production.sheet_qty = criteria_amount_id.amount
                    break


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

    def _compute_real_total_cost(self):
        
        for production in self:
            production.real_total_cost = sum(production.workorder_ids.mapped('real_total_cost'))
            
    @api.model
    def create(self, values):
        product_code = self.env['product.product'].browse(values['product_id']).product_tmpl_id.default_code
        project_code = self.env['project.project'].browse(values['project_id']).code
        max_internal_by_project_id = 1
        max_production_id = self.env['mrp.production'].search([('project_id', '=', values['project_id']), ('internal_by_project_id', '!=', False)], order='internal_by_project_id desc', limit=1) 

        if max_production_id:
            if max_production_id.internal_by_project_id > 0:
                max_internal_by_project_id = max_production_id.internal_by_project_id + 1
            else:
                _logger.error('Esta vacio el id')
        else:
            _logger.error('Esta vacio el resultado')

        year_week = datetime.now().strftime("%V").zfill(2) + '/' + datetime.now().strftime("%y").zfill(2)

        code = product_code + '/' + str(project_code).zfill(4) + '/' + str(max_internal_by_project_id).zfill(2) + '/' + year_week
        values['internal_by_project_id'] = max_internal_by_project_id
        values['code'] = code
        result = super(MrpProduction, self).create(values)

        computation_criterias = self.env['mrp.computation.criteria'].search([])
        for cc in computation_criterias:
            self.env['mrp.production.criteria.amount'].create({
                'computation_criteria_id': cc.id,
                'production_id': result.id,
            })
        
        return result

    def write(self, values):
        if 'custom_state' in values and values['custom_state'] == 'done':
            values['date_finished'] = datetime.now()
        if 'custom_state' in values and values['custom_state'] == 'loaded':
            values['date_loaded'] = datetime.now()
        return super(MrpProduction, self).write(values)

    @api.onchange('product_id', 'picking_type_id', 'company_id')
    def onchange_product_id(self):
        super(MrpProduction, self).onchange_product_id()
        if self.product_id and not self.bom_id:
            self.set_default_pricelist()
    
    def set_default_pricelist(self):
        default_bom_id = self.env['mrp.bom'].search([('is_default_pricelist', '=', True)], limit=1)
        if default_bom_id:
            self.bom_id = default_bom_id.id

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
    out_date = fields.Datetime(string="Fecha de salida")
    in_date = fields.Datetime(string="Fecha de entrada")
    qty_frame = fields.Integer(string="Nº de unidades")
    qty_sheet = fields.Integer(string="Nº de hojas")
    notes = fields.Text('Notes')
    production_id = fields.Many2one(string="Orden de producción", comodel_name="mrp.production", inverse_name="varnish_ids")

class MrpAluminumColor(models.Model):
    _name = 'mrp.aluminum.color'
    
    name = fields.Char('Nombre')
