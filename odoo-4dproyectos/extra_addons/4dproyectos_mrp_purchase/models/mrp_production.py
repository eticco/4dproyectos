# -*- coding: utf-8 -*-
from odoo import models, fields, api


class MrpProduction(models.Model):
    _inherit = 'mrp.production'
    
    purchase_ids   = fields.One2many(comodel_name="purchase.order", inverse_name="production_id", string="Pedidos de compra")
    purchase_count = fields.Integer(string="Nº de pedidos", compute="compute_purchase_count")

    def compute_purchase_count(self):
        for production in self:
            production.purchase_count = len(production.purchase_ids)

    def action_view_po(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id("purchase.purchase_rfq")
        action['domain'] = [('production_id', 'in', self.ids)]
        action['context'] = {'default_production_id' : self.id}
        return action