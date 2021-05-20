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

    employee_text     = fields.Char(string="Empleado", required=True)
    production_text   = fields.Char(string="Orden de producción", required=True)
    workorder_text    = fields.Char(string="Orden de trabajo", required=True)

    employee_id     = fields.Many2one(comodel_name="hr.employee", string="Empleado", required=True)
    production_id   = fields.Many2one(comodel_name="mrp.production", string="Orden de producción", required=True)
    workorder_id    = fields.Many2one(comodel_name="mrp.workorder", string="Orden de trabajo", required=True)
    user_id         = fields.Many2one(comodel_name="res.users", related="employee_id.user_id", string="Usuario")
    productivity_id = fields.Many2one(comodel_name="mrp.workcenter.productivity", string="Seguimiento de tiempo")
    finish_order    = fields.Boolean(string="Finalizar la orden", default=False)

    @api.onchange('employee_text')
    def onchange_calculate_employee_id(self):
        if self.employee_text:
            self.employee_id = self.env['hr.employee'].search([('name', '=', self.employee_text)], limit=1)
        self.calculate_productivity_id()

    @api.onchange('production_text')
    def onchange_calculate_production_id(self):
        if self.production_text:
            replaced_name = self.production_text.replace("-", "/")
            self.production_id = self.env['mrp.production'].search([('code', '=', replaced_name)], limit=1)

    @api.onchange('workorder_text')
    def onchange_calculate_workorder_id(self):
        if self.workorder_text:
            self.workorder_id = self.env['mrp.workorder'].search([('workcenter_name', '=', self.workorder_text),('production_id', '=', self.production_id.id), ('state', '!=', 'done')], limit=1)
        self.calculate_productivity_id()

    @api.onchange('production_id')
    def onchange_clean_workorder_id(self):
        self.workorder_id = False

    def calculate_productivity_id(self):
        self.productivity_id = False
        _logger.error('calculate_productivity_id')

        if self.workorder_id and self.user_id:
            _logger.error('tiene datos')
            domain = [
                ('user_id', '=', self.user_id.id),
                ('date_end', '=', False),
            ]
            productivity_ids = self.env['mrp.workcenter.productivity'].search(domain)
            if len(productivity_ids) <= 0:
                _logger.error('no tiene productivity_ids para %s', self.user_id.id)
            other_productivity_ids = productivity_ids.filtered(lambda r: r.workorder_id != self.workorder_id)
            if other_productivity_ids:
                _logger.error('doy excepcion')
                other_workorder_id = other_productivity_ids[0].workorder_id
                raise Warning('El empleado ya tiene un parte para la orden de trabajo %s de la orden de produccion %s' %(other_workorder_id.display_name, other_workorder_id.production_id.name))
            elif len(productivity_ids):
                _logger.error('tiene productivity_ids')
                self.productivity_id = productivity_ids[0].id
    
    def action_charge_hours(self):
        _logger.error('Estoy cargando horas...')
        _logger.error("En la orden %s", self.production_id)
        _logger.warn("En la workorder %s", self.workorder_id)
        _logger.warn("En el empleado %s", self.employee_id)
        _logger.warn("En el usuario %s", self.user_id)

        if not self.productivity_id:
            self.workorder_id.with_context(charge_user=self.user_id.id).button_start()
        else:
            if self.finish_order:
                self.workorder_id.button_finish()
            else:
                self.workorder_id.button_pending()
        self.employee_text = False
        self.production_text = False
        self.workorder_text = False
        self.production_id = False
        self.workorder_id = False

        return True