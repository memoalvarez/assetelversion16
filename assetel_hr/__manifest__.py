# -*- coding: utf-8 -*-
{
    'name': "Assetel HR",

    'summary': """
        Adecuaciones para HR Assetel""",

    'description': """
        Adecuaciones para HR Assetel
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
    'depends': ['base', 'hr_holidays'],

    # always loaded
    'data': [
        'views/hr_leave_type.xml',
        'views/hr_leave.xml',
    ],
}