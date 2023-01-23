# -*- coding: utf-8 -*-
{
    'name': "CRM Porcentaje Por Etapas Fix",

    'summary': "Define porcentaje por etapas en el CRM",

    'description': """
        Flujo de registro de clientes
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
    "depends": ["crm"],

    # always loaded
    "data": [
        "views/crm_stage.xml",
    ],
}