# -*- coding: utf-8 -*-
{
    'name': "Modificacion a approval requet",

    'summary': """
        Modificacion a approval requet""",

    'description': """
        Modificacion a approval requet
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
    'depends': ['base', 'approvals'],

    # always loaded
    'data': [
        'views/approval_request_category_menu.xml',
        'views/approval_request_category.xml',
        'views/approval_request.xml',
    ],
}
