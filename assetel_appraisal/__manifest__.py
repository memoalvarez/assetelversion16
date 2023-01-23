# -*- coding: utf-8 -*-
{
    'name': "Evaluaciones Assetel",

    'summary': """
        Evaluaciones assetel""",

    'description': """
        Evaluaciones assetel
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
    'depends': ['base', 'hr'],

    # always loaded
    'data': [
        'data/ir_sequence_data.xml',
        'data/mail_activity_data.xml',
        'views/appraisal_behavior.xml',
        'views/appraisal_period_menu.xml',
        'views/appraisal_period_template.xml',
        'views/appraisal_period.xml',
        'views/appraisal_smart.xml',
        'views/email_appraisal_period.xml',
        'views/expected_behaviors.xml',
        'views/strategic_objectives.xml',
    ],
}
