# -*- coding: utf-8 -*-
{
    'name': "Vacaciones assetel",

    'summary': """
        Modificación a modulo hr holidays""",

    'description': """
        Modificación a modulo hr holidays
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
    'depends': ['base', 'hr_holidays', 'hr_payroll'],

    # always loaded
    'data': [
        'views/hr_leave_type.xml',
        'data/assetel_holidays_data.xml',
    ],
}
