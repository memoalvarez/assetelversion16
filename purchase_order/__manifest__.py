# -*- coding: utf-8 -*-
{
    'name': "Orden de compra assetel",

    'summary': """
        Orden de compra assetel""",

    'description': """
        Orden de compra assetel
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
    'depends': ['base', 'purchase',],

    # always loaded
    'data': [
        'views/purchase_order.xml',
        'views/template_purchase_order.xml',
    ],
}
