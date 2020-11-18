# -*- coding: utf-8 -*-
# Este fichero carga configuración de Odoo
{
    'name' : 'Eticco Skin',
    'description' : """
        Skin personalizado para odoo
    """,
    'depends' : ['base'],
    'data' : [
        'views/eticco_header_inherit_view.xml'
    ],
    'author' : 'Javier Fernandez',
    'installable' : True,
    'auto_install' : False,
    'application' : True,
}