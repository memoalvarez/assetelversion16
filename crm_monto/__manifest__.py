# -*- coding: utf-8 -*-
{
    'name': "CRM Monto de Retencion",

    'summary': "CRM campo de monto de retencion",

    'description': """
        CRM campo de monto de retencion
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
    "depends": ['base','crm'],

    # always loaded
    "data": [
        "views/crm_lead.xml",
    ],
}