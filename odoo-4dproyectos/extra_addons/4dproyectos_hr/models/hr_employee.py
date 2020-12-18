# -*- coding: utf-8 -*-
from odoo import models, api


class HrEmployee(models.Model):
    _inherit = 'hr.employee'
    
    def write(self, values):
        result = super(HrEmployee, self).write(values)
        if values.get('job_id', False):
            for employee in self:
                employee.timesheet_cost = employee.env['hr.job'].browse(values.get('job_id')).timesheet_cost
        return result