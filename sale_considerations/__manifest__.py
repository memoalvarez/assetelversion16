# -*- coding: utf-8 -*-
{
    'name': "Consideraciones de venta",

    'summary': """
        Consideraciones de venta""",

    'description': """
        Consideraciones de venta
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
        'views/sale_considerations.xml',
        'views/sale_considerations_menu.xml',
        'views/sale_order.xml',
    ],
}