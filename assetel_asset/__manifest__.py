# -*- coding: utf-8 -*-
{
    'name': "Assetel asset",

    'summary': """
        Assetel asset""",

    'description': """
         Assetel asset
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
    'depends': ['base', 'account_asset'],

    # always loaded
    'data': [
        'views/account_asset.xml',
    ],
}
