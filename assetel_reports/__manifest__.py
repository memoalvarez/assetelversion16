# -*- coding: utf-8 -*-
{
    'name': "Reportes Assetel",

    'summary': """
        Reportes Assetel""",

    'description': """
        Reportes Assetel
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
    'depends': ['base', 'installed_services', 'mrp', 'service_sizing'],

    # always loaded
    'data': [
        'views/account_move.xml',
        'views/installed_services.xml',
        'views/residencial_template.xml',
        'views/sale_order.xml',
        'views/templates.xml',
        'views/stock_picking.xml',
        'views/sign_template.xml',
        'views/sign_request.xml',
        'views/responsive_template.xml',
    ],
}
