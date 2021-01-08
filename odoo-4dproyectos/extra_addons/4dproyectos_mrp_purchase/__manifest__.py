# -*- coding: utf-8 -*-
{
    'name': "4D Mrp Purchase",
    'summary': """Compras para las órdenes de fabricación""",
    'author': "Eticco Freelosophy",
    'license': 'AGPL-3',
    'website': "",
    'category': 'Eticco',
    'version': '14.0.1',
    'depends': [
        'mrp',
        'purchase',
    ],
    'data': [
            'views/mrp_production_view.xml',
            'views/purchase_order_view.xml',
    ],
    'demo': [],
    'application': False,
    'installable': True
}
