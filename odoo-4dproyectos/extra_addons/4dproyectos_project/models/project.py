# -*- coding: utf-8 -*-

from odoo import api, models, fields
import logging
_logger = logging.getLogger(__name__)

class Project(models.Model):
    _inherit = 'project.project'

    partner_shipping_id = fields.Many2one('res.partner', string='Dirección')
    total_budget = fields.Float(string="Presupuesto total", currency_field='currency_id')
    raw_material_cost = fields.Float(string="Coste materias primas")
    status = fields.Selection(string="Estado", selection=[('contratada', 'Contratada'), ('en_ejecucion', 'En ejecución'), ('terminada_en_fabrica', 'Terminada en fábrica'), ('entregada', 'Entregada'), ('facturada', 'Facturada'), ('cerrada', 'Cerrada')])
    start_date = fields.Date(string="Fecha de alta")
