# -*- coding: utf-8 -*-
{
    'name': "4D Proyectos Cargar horas",
    'summary': """Personalización de carga de horas de 4D Proyectos""",
    'author': "Eticco Freelosophy",
    'license': 'AGPL-3',
    'website': "",
    'category': 'Eticco',
    'version': '14.0.1',
    'depends': [
        '4dproyectos_mrp',
        'web',
    ],
    'data': [
            'data/groups.xml',
            'data/ir_config_parameter.xml',
            'security/ir.model.access.csv',
            'views/charge_hours_wizard_view.xml',
            'views/head.xml',
    ],
    'demo': [],
    'application': False,
    'installable': True
}
