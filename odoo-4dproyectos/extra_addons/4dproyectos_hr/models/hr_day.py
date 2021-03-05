# -*- coding: utf-8 -*-
from odoo import models, fields, api
import datetime

class HrDay(models.Model):
    _name = 'hr.day'
    _rec_name = 'date'
    
    date = fields.Date(string="Fecha", required=True)
    attendance_ids = fields.One2many(comodel_name="hr.attendance", inverse_name="hr_day_id", string="Asistencias")
    account_analytic_line_ids = fields.One2many(comodel_name="account.analytic.line", inverse_name="hr_day_id", string="Partes de horas")
    total_attendance = fields.Float(string="Total asistencias (h)", compute="_compute_total_attendance")
    total_worked = fields.Float(string="Total partes de horas (h)", compute="_compute_total_worked")
    employee_id = fields.Many2one(comodel_name="hr.employee", string="Empleado")

    @api.depends('attendance_ids', 'attendance_ids.worked_hours')
    def _compute_total_attendance(self):
        for day in self:
            attended_hours = 0.0
            for attendance in day.attendance_ids:
                attended_hours += attendance.worked_hours
            day.total_attendance = attended_hours

    @api.depends('account_analytic_line_ids', 'account_analytic_line_ids.unit_amount')
    def _compute_total_worked(self):
        for day in self:
            worked_hours = 0.0
            for line in day.account_analytic_line_ids:
                worked_hours += line.unit_amount
            day.total_worked = worked_hours


class HrAttendance(models.Model):
    _inherit = 'hr.attendance'
    
    hr_day_id = fields.Many2one(comodel_name="hr.day", string="Día")
    
    @api.model
    def create(self, values):
        day_model = self.env['hr.day']
        check_in_date = datetime.datetime.strptime(values['check_in'], "%Y-%m-%d %H:%M:%S").date()
        day = day_model.search([('date', '=', str(check_in_date)),('employee_id', '=', values['employee_id'])], limit=1)
        if day:
            values['hr_day_id'] = day.id
        else:
            values['hr_day_id'] = day_model.create({'date': str(check_in_date),
                                                    'employee_id': values['employee_id']}).id
        return super(HrAttendance, self).create(values)

class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'
    
    hr_day_id = fields.Many2one(comodel_name="hr.day", string="Día")

    @api.model
    def create(self, values):
        day_model = self.env['hr.day']
        day = day_model.search([('date', '=', values['date']),('employee_id', '=', values['employee_id'])], limit=1)
        if day:
            values['hr_day_id'] = day.id
        else:
            values['hr_day_id'] = day_model.create({'date': values['date'],
                                                    'employee_id': values['employee_id']}).id
        return super(AccountAnalyticLine, self).create(values)