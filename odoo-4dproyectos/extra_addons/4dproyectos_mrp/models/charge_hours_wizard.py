# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import Warning
import logging
_logger = logging.getLogger(__name__)

class ChargeHoursWizard(models.TransientModel):
    _name = 'charge.hours.wizard'
    
    @api.model
    def default_employee_id(self):
        employee_id = self.env['hr.employee'].search([('user_id', '=', self.env.user.id)], limit=1)
        return employee_id

    production_id   = fields.Many2one(comodel_name="mrp.production", string="Orden de producción", required=False)
    workorder_id    = fields.Many2one(comodel_name="mrp.workorder", string="Orden de trabajo", required=False)
    employee_id     = fields.Many2one(comodel_name="hr.employee", string="Empleado", default=default_employee_id, required=True)
    user_id         = fields.Many2one(comodel_name="res.users", related="employee_id.user_id", string="Usuario")
    productivity_id = fields.Many2one(comodel_name="mrp.workcenter.productivity", string="Seguimiento de tiempo")
    finish_order    = fields.Boolean(string="Finalizar la orden", default=False)

    @api.onchange('production_id')
    def onchange_clean_workorder_id(self):
        self.workorder_id = False

    @api.onchange('workorder_id', 'user_id')
    def onchange_calculate_productivity_id(self):
        self.productivity_id = False
        if self.workorder_id and self.user_id:
            domain = [
                ('user_id', '=', self.user_id.id),
                ('date_end', '=', False),
            ]
            productivity_ids = self.env['mrp.workcenter.productivity'].search(domain)
            other_productivity_ids = productivity_ids.filtered(lambda r: r.workorder_id != self.workorder_id)
            if other_productivity_ids:
                raise Warning('El empleado ya tiene un parte para la orden de trabajo %s' %(other_productivity_ids[0].workorder_id.display_name))
            elif len(productivity_ids):
                self.productivity_id = productivity_ids[0].id
    
    def action_charge_hours(self):
        _logger.error('action_charge_hours')
        _logger.error(self.production_id)
        _logger.warn(self.workorder_id)
        _logger.warn(self.employee_id)

        if not self.productivity_id:
            self.workorder_id.button_start()
        else:
            if self.finish_order:
                self.workorder_id.button_finish()
            else:
                self.workorder_id.button_pending()
        self.production_id = False
        self.workorder_id = False

        return True