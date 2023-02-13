# -*- coding: utf-8 -*-
{
    'name': "Portal Partner",

    'summary': """
        Modificaciones para adaptar portal de partners""",

    'description': """
        Modificaciones para adaptar portal de partners
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
    'depends': ['base', 'website_crm_partner_assign', 'crm', 'sale_management', 'portal'],

    # always loaded
    'data': [
        'views/crm_stage.xml',
        'views/partner_portal.xml',
        'views/sale_order.xml',
    ],
}
