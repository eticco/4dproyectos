# -*- coding: utf-8 -*-
from odoo import models, fields, api


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    hr_day_ids = fields.One2many(comodel_name="hr.day", inverse_name="employee_id", string="Listado de días")
    day_count = fields.Integer(string="Comparativa (h)", compute="_compute_day_count")

    # Añado aquí los campos para timesheet_cost para evitar tener que instalar el módulo hr_timesheet
    # Si lo instalamos hay que ocultar muchas cosas para no confundir los hr_timesheet con los mrp_workcenter_productivity
    timesheet_cost = fields.Monetary('Coste del parte de horas', currency_field='currency_id', groups="hr.group_hr_user", default=0.0)
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id', readonly=True)
    
    def write(self, values):
        result = super(HrEmployee, self).write(values)
        if values.get('job_id', False):
            for employee in self:
                employee.timesheet_cost = employee.env['hr.job'].browse(values.get('job_id')).timesheet_cost
        return result

    def _compute_day_count(self):
        for employee in self:
            employee.day_count = len(employee.hr_day_ids)