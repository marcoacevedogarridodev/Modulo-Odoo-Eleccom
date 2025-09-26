{
    'name': 'Eleccom',
    'version': '16.0.1.0.0',
    'category': 'Human Resources',
    'summary': 'Personalización de vista lista de empleados con columnas adicionales',
    'author': 'Mag',
    'depends': ['hr', 'web'],
    'data': [
        'security/security.xml',         
        'security/ir.model.access.csv',
        'views/hr_employee_views.xml',
        'reports/contrato_reports.xml',
        'reports/contrato_indefinido_reports.xml',
        'data/contrato_actions.xml',  
        'data/users.xml',                
    ],
    'assets': {
        'web.assets_backend': [
            'eleccom/static/src/css/hide_fields.css',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
