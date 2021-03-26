# -*- coding: utf-8 -*-
from odoo import models, fields, api


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    hr_day_ids = fields.One2many(comodel_name="hr.day", inverse_name="employee_id", string="Listado de días")
    day_count = fields.Integer(string="Comparativa (h)", compute="_compute_day_count")
    
    def write(self, values):
        result = super(HrEmployee, self).write(values)
        if values.get('job_id', False):
            for employee in self:
                employee.timesheet_cost = employee.env['hr.job'].browse(values.get('job_id')).timesheet_cost
        return result

    def _compute_day_count(self):
        for employee in self:
            employee.day_count = len(employee.hr_day_ids)