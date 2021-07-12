# -*- coding: utf-8 -*-
{
    'name': "4D Proyectos Modificar menú",
    'summary': """Personalización del menú principal para 4D Proyectos""",
    'author': "Eticco Freelosophy",
    'license': 'AGPL-3',
    'website': "",
    'category': 'Eticco',
    'version': '14.0.1',
    'depends': [
        'base',
        'mail',
        'calendar',
        'contacts',
        'crm',
        'stock',
        'project',
        'mrp',
        'hr',
        'hr_attendance',
        'maintenance',
    ],
    'data': [
            'views/main_menu_view.xml',
    ],
    'demo': [],
    'application': False,
    'installable': True
}
