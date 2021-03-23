# -*- coding: utf-8 -*-
{
    'name': "4D Proyectos Hr",
    'summary': """Personalización de RRHH de 4D Proyectos""",
    'author': "Eticco Freelosophy",
    'license': 'AGPL-3',
    'website': "",
    'category': 'Eticco',
    'version': '14.0.1',
    'depends': [
		'hr_attendance',
        'hr_timesheet',
        '4dproyectos_mrp',
    ],
    'data': [
            'security/ir.model.access.csv',
            'views/hr_job_view.xml',
            'views/hr_employee_view.xml',
            'views/hr_day_view.xml',
        
    ],
    'demo': [],
    'application': False,
    'installable': True
}
