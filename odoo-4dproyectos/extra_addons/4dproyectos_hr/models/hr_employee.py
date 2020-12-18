# -*- coding: utf-8 -*-
from odoo import models, api


class HrEmployee(models.Model):
    _inherit = 'hr.employee'
    
    @api.model
    def write(self, values):
        if values.get('job_id', False):
            values['timesheet_cost'] = self.env['hr.job'].browse(values.get('job_id')).timesheet_cost
        result = super(HrEmployee, self).write(values)
        return result
