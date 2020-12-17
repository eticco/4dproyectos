# -*- coding: utf-8 -*-
# Agregar todos los addons necesarios como base
{
    'name': "Éticco Unattended Install",
    'images': [],
    'summary': """Instalación de módulos necesarios""",
    'author': "Eticco Freelosophy",
    'license': 'AGPL-3',
    'website': "",
    'category': '',
    'version': '14.0.1',
    'depends': [
        'base',
        'crm',
		'hr_attendance',
		'hr_timesheet',
		'maintenance',
        'mrp',
        'project',
        'stock',
    ],
    'data': [],
    'demo': [],
    'application': False,
    'installable': True
}
