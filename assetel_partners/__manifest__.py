# -*- coding: utf-8 -*-
{
    'name': "Assetel Partners",

    'summary': """
        Assetel partners""",

    'description': """
        Assetel partners""",

    'author': "Assetel",
    'website': "http://www.assetel.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',
    'license': 'LGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['base', 'website_crm_partner_assign', 'contacts', 'sign', 'survey', 'base_address_extended', 'base_address_city'], 

    # always loaded
    'data': [
        'data/ir_sequence_data.xml',
        'views/res_partner.xml',
        'views/assetel_partners_menu.xml',
        'views/assetel_partners_stage.xml',
        'views/assetel_partners.xml',
        'views/sign_request.xml',
        'views/sign_send_request.xml',
        'views/survey_invite.xml',
        ],

}