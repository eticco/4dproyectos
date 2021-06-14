# -*- coding: utf-8 -*-
{
    'name': 'Informes 4D',
    'version': '1.0',
    'category': 'Reporting',
    'license': 'AGPL-3',
    'summary': 'Informes 4D Proyectos',
    'author': 'Eticco Freelosophy',
    'website': 'https://www.eticco.es',
    'depends': [
        'mrp',
    ],
    'data': [   
            'reports/employee_id_report.xml',
            'reports/production_order_report.xml', 
            'reports/reports.xml', 
            'reports/report_templates.xml', 
            'reports/header.xml', 
            'reports/paperformat_production_order.xml',
            'reports/workcenter_report.xml'
            
            ],
    'installable': True,
}
