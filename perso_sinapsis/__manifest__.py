# -*- coding: utf-8 -*-
{
    'name': "Perso Sinapsis",

    'summary': """
        Personalizaciones especificas para Sinapsis""",

    'description': """

        Personalizaciones especificas para Sinapsis

    """,

    'author': "Nanobytes Informatica y Telecomunicaciones S.L.",
    'website': "",
    'category': 'perso',
    'version': '1.0',
    'depends': ['web', 'hr_timesheet', 'project', 'project_enterprise'],
    'data': [
        'data/data.xml',
        'data/views.xml',
        'views/task_views.xml'
    ],
    'qweb': [],
    'installable': True,
    'application': True,
}
