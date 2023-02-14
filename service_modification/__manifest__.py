# -*- coding: utf-8 -*-
{
    'name': "Modificacion de servicio",

    'summary': """
        Modificacion de servicio""",

    'description': """
        Modificacion de servicio
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
    'depends': ['base', 'service_installation'],

    # always loaded
    'data': [
        'views/project_task.xml',
        'views/sale_subscription.xml',
    ],
}
