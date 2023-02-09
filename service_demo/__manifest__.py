# -*- coding: utf-8 -*-
{
    'name': "Demo",

    'summary': """
        Demo""",

    'description': """
        Demo
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
    'depends': ['base', 'installed_services'],

    # always loaded
    'data': [
        'views/project_task.xml',
        'views/crm_lead.xml',
        'views/crm_stage.xml',
        'views/mail_activity_type.xml',
        'views/installed_services.xml',
        'views/res_config_settings.xml',
    ],
}
