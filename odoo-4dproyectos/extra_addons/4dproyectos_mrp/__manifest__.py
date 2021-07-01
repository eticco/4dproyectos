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
        '4dproyectos_hr',
        'mrp',
    ],
    'data': [
            'data/computation_criteria_data.xml',
            'data/groups.xml',
            'security/ir.model.access.csv',
            'views/mrp_production_view.xml',
            'views/mrp_workorder_view.xml',
            'views/mrp_workcenter_view.xml',
            'views/charge_hours_wizard_view.xml',
            'views/mrp_bom_view.xml',
            'views/varnish_view.xml',
            'views/mrp_routing_workcenter_view.xml',
    ],
    'demo': [],
    'application': False,
    'installable': True
}
