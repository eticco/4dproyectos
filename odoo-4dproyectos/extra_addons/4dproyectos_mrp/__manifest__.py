# -*- coding: utf-8 -*-
{
    'name': "4D Proyectos Mrp",
    'summary': """Personalización de fabricación de 4D Proyectos""",
    'author': "Eticco Freelosophy",
    'license': 'AGPL-3',
    'website': "",
    'category': 'Eticco',
    'version': '14.0.1',
    'depends': [
        'mrp',
    ],
    'data': [
            'data/computation_criteria_data.xml',
            'security/ir.model.access.csv',
            'views/mrp_production_view.xml',
            'views/mrp_workcenter_view.xml',
            'views/charge_hours_wizard_view.xml',
    ],
    'demo': [],
    'application': False,
    'installable': True
}
