# -*- coding: utf-8 -*-
{
    'name': "Emite una alerta cuando intentamos emitir una factura con fecha anterior a la ultima emitida y validada",

    'summary': """""",

    'description': """
        Emite una alerta cuando intentamos emitir una factura con fecha anterior a la ultima emitida y validada
    """,

    'author': "ProcessControl",
    'website': "http://www.processcontrol.es",
    'category': 'Revenues',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','contacts','account'],

    # always loaded
    'data': [
        'wizard/alert_wizard.xml',
        #'security/ir.model.access.csv',
        # 'views/views.xml',
    ]
    # only loaded in demonstration mode
    #'demo': [
        #'demo/demo.xml',
    #],
}
