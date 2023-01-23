# -*- coding: utf-8 -*-
{
    'name': "Historial de suscripciones",

    'summary': """
        Historial de suscripciones""",

    'description': """
        Historial de suscripciones
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
    'depends': ['base', 'sale_subscription','installed_services'],

    # always loaded
    'data': [
        'views/sale_subscription.xml',
        'views/history_sale_subscription.xml',
        'views/subscription_lines.xml',
        'views/subscription_lines_menu.xml',
    ],
}
