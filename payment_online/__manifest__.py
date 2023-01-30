# -*- coding: utf-8 -*-
{
    'name': "Pago en linea faturas",

    'summary': """
        Pago en linea faturas""",

    'description': """
        Pago en linea faturas
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
    'depends': ['base', 'contacts', 'account_accountant', 'account_payment'],

    # always loaded
    'data': [
        'views/account_move.xml',
        'views/res_partner.xml',
        'views/website_invoice.xml',
    ],
}
