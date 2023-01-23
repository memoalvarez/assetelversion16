# -*- coding: utf-8 -*-
{
    'name': "Grupo corporativo",

    'summary': """
        Grupo corporativo""",

    'description': """
        Grupos corporativo
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
    'depends': ['base', 'contacts', 'sale_subscription', 'installed_services'],

    # always loaded
    'data': [
        'views/res_partner.xml',
        'views/sale_subscription.xml',
    ],
}