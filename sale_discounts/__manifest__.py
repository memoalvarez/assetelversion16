# -*- coding: utf-8 -*-
{
    'name': "Descuento en orden de venta",

    'summary': """
        Descuento en orden de venta""",

    'description': """
        Descuento en orden de venta
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
    'depends': ['base', 'stock', 'sale_management'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/sale_order.xml',
    ],
}
