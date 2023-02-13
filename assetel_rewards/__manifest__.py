# -*- coding: utf-8 -*-
{
    'name': "Assetel rewards",

    'summary': """
        Assetel rewards""",

    'description': """
        Assetel rewards
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
    'depends': ['base', 'hr',  'hr_gamification'],

    # always loaded
    'data': [
        'views/gamification_badge_user.xml',
        'views/gamification_badge_user_menu.xml',
        'views/gamification_badge_user_wizard.xml',
    ],
}
