# -*- coding: utf-8 -*-
{
    'name': "Permite añadir a un contacto multiples direcciones de facturación",

    'summary': """""",

    'description': """
        Permite añadir a un contacto multiples direcciones de facturación
    """,

    'author': "ProcessControl",
    'website': "http://www.processcontrol.es",
    'category': 'Revenues',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','contacts'],

    # always loaded
    'data': [
        #'security/ir.model.access.csv',
        'views/views.xml',
    ]
    # only loaded in demonstration mode
    #'demo': [
        #'demo/demo.xml',
    #],
}
