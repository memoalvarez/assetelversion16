# -*- coding: utf-8 -*-
{
    'name': "Historial de servicios",

    'summary': """
        Historial de servicios""",

    'description': """
        Historial de servicios
    """,

    'author': "Assetel",
    'website': "http://www.assetel.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '1',
    'license': 'LGPL-3',


    # any module necessary for this one to work correctly
    'depends': ['base', 'service_modification', 'service_demo'],

    # always loaded
    'data': [
        'views/history_installed_services.xml',
        'views/history_service_information.xml',
        'views/installed_services.xml',
    ],
}
