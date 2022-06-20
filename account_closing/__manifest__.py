# -*- coding: utf-8 -*-
{
    'name': "account_closing",

    'summary': """
        Módulo para cierres contables""",

    'author': "Nanobytes Informatica y Telecomunicaciones S.L.",
    'website': "https://nanobytes.es/",

    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account_accountant'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'wizards/account_closing_wizard_view.xml',
    ],
}
