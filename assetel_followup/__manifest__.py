# -*- coding: utf-8 -*-
{
    'name': "Seguimiento Assetel",

    'summary': """
        Seguimiento Assetel""",

    'description': """
        Seguimiento Assetel
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
    'depends': ['base', 'assetel_reports', 'account_accountant'],

    # always loaded
    'data': [
        'views/email_followup.xml',
        'views/res_partner.xml',
    ],
}
