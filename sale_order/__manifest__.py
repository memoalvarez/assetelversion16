# -*- coding: utf-8 -*-
{
    'name': "Sale Order Assetel",

    'summary': """
        Modificacion a sale order""",

    'description': """
        Modificacion a sale order
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
    'depends': ['base', 'sale_management'],

    # always loaded
    'data': [
        'views/sale_order.xml',
    ],
}
