# -*- coding: utf-8 -*-
{
    'name': "Permisos Assetel",

    'summary': """
        Esto crea grupos para los permimsos en algunas acciones""",

    'description': """
        Esto crea grupos para los permimsos en algunas acciones
    """,

    'author': "Assetel",
    'website': "http://www.assetel.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',
    'license': 'LGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/user_groups.xml',
    ],
}