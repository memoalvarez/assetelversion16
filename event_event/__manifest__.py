# -*- coding: utf-8 -*-
{
    'name': "Eventos Assetel",

    'summary': """
        Modificacion a event event""",

    'description': """
        Modificacion a event event
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
    'depends': ['base', 'website_event'],

    # always loaded
    'data': [
        'views/event_event.xml',
        'views/event_registration.xml',
    ],
}
