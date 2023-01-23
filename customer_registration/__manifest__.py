# -*- coding: utf-8 -*-
{
    'name': "Registro de clientes",

    'summary': """
        Flujo de registro de clientes""",

    'description': """
        Flujo de registro de clientes
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
    'depends': ['base', 'crm', 'installed_services', 'survey'],

    # always loaded
    'data': [
        'views/crm_lead.xml',
        'views/helpdesk_team.xml',
        'views/helpdesk_ticket.xml',
        'views/res_config_settings.xml',
        'views/survey_invite.xml',
    ],
}
