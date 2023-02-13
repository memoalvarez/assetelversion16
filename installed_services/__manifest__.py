# -*- coding: utf-8 -*-
{
    'name': "Servicios instalados",

    'summary': """
        Servicios instalados""",

    'description': """
        Servicios instalados
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
    'depends': ['base', 'stock', 'customer_site', 'mrp'],

    # always loaded
    'data': [
        'views/account_move.xml',
        'views/helpdesk_ticket.xml',
        'views/installed_services_menu.xml',
        'views/installed_services.xml',
        'views/product_product.xml',
        'views/res_partner.xml',
        'views/sale_order.xml',
        'views/service_information_menu.xml',
        'views/service_information.xml',
        'views/stock_production_lot.xml',
        'data/ir_sequence_data.xml',
    ],
}
