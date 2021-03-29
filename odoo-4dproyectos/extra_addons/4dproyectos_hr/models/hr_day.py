# -*- coding: utf-8 -*-
from odoo import models, fields, api
import datetime

class HrDay(models.Model):
    _name = 'hr.day'
    _rec_name = 'date'
    
    date = fields.Date(string="Fecha", required=True)
    attendance_ids = fields.One2many(comodel_name="hr.attendance", inverse_name="hr_day_id", string="Asistencias")
    mrp_workcenter_productivity_ids = fields.One2many(comodel_name="mrp.workcenter.productivity", inverse_name="hr_day_id", string="Partes de horas")
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

    @api.depends('mrp_workcenter_productivity_ids', 'mrp_workcenter_productivity_ids.duration')
    def _compute_total_worked(self):
        for day in self:
            worked_hours = 0.0
            for productivity in day.mrp_workcenter_productivity_ids:
                worked_hours += productivity.duration
            day.total_worked = worked_hours / 60.0


class HrAttendance(models.Model):
    _inherit = 'hr.attendance'
    
    hr_day_id = fields.Many2one(comodel_name="hr.day", string="Día")

    def create_day_record(self, values):
        day_model = self.env['hr.day']
        check_in = values['check_in']
        day = False
        if 'search_default_today' in self.env.context:
            check_in_date = datetime.datetime.strptime(check_in, "%Y-%m-%d %H:%M:%S").date()
            day = day_model.search([('date', '=', str(check_in_date)),
                                ('employee_id', '=', values['employee_id'])], limit=1)
        if day:
            values['hr_day_id'] = day.id
        else:
            values['hr_day_id'] = day_model.create({'date': str(check_in),
                                                    'employee_id': values['employee_id']}).id
            check_in_date = check_in #datetime.datetime.strptime(check_in, "%Y-%m-%d %H:%M:%S").date()
            day = day_model.search([('date', '=', str(check_in_date)),
                                    ('employee_id', '=', values['employee_id'])], limit=1)
            if day:
                values['hr_day_id'] = day.id
            else:
                values['hr_day_id'] = day_model.create({'date': str(check_in_date),
                                                        'employee_id': values['employee_id']}).id
        return values

    @api.model
    def create(self, values):
        values = self.create_day_record(values)
        return super(HrAttendance, self).create(values)

class MrpWorkcenterProductivity(models.Model):
    _inherit = 'mrp.workcenter.productivity'
    
    hr_day_id = fields.Many2one(comodel_name="hr.day", string="Día")

    def create_day_record(self, values):
        day_model = self.env['hr.day']
        employee_id = self.search_employee_from_user(values['user_id'])
        if not employee_id:
            return values
        day = day_model.search([('date', '=', values['date_start']),
                                ('employee_id', '=', employee_id.id)], limit=1)
        if day:
            values['hr_day_id'] = day.id
        else:
            values['hr_day_id'] = day_model.create({'date': values['date_start'],
                                                    'employee_id': employee_id.id}).id
        return values

    @api.model
    def create(self, values):
        values = self.create_day_record(values)
        return super(MrpWorkcenterProductivity, self).create(values)

    def search_employee_from_user(self, user):
        return self.env['hr.employee'].search([('user_id', '=', user)]) or False