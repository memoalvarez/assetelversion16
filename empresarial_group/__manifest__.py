# -*- coding: utf-8 -*-
{
    'name': "Grupos empresariales",

    'summary': """
        Grupos empresariales""",

    'description': """
        Grupos empresariales
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
    'depends': ['base', 'contacts', 'helpdesk', 'sale_management', 'sale_subscription'],

    # always loaded
    'data': [
        'views/empresarial_group_menu.xml',
        'views/empresarial_group.xml',
        'views/helpdesk_ticket.xml',
        'views/res_partner.xml',
        'views/sale_order.xml',
        #'views/sale_subscription.xml',
    ],
}