# -*- coding: utf-8 -*-
{
    'name': "San Miguel - Reporte Diario",

    'summary': """
        Reporte Diario""",

    'description': """
        Movientos diarios de productos
    """,

    'author': "Recicladora San Miguel",
    'website': "https://www.recicladorasanmiguel.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'purchase', 'purchase_order_modifications', 'mail'],

    # always loaded
    'data': [
        'views/reporte_diario.xml',
        'views/product.xml',
        'data/cronjobs.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}