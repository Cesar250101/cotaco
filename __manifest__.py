# -*- coding: utf-8 -*-
{
    'name': "cotaco",

    'summary': """
        Localización Odoo para la empresa Cotaco""",

    'description': """
        Modificación modelo lista precios, se agrega campo comisión por listas de precios
        Agrega modelo tabla comision y factorización
    """,

    'author': "Method",
    'website': "http://www.openmethod.cl",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/11.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','account','sale_exception','stock','mrp','crm','hr','mrp_repair','quality_control'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/armado.xml',
        'views/compras.xml',
        'views/produccion.xml',
        'views/contabilidad.xml',
        'views/inventario.xml',
        'views/nomina.xml',
        'views/productos.xml',
        'views/ventas.xml',
        'views/templates.xml',
        'views/empleados.xml',
        'data/exception_rule_data.xml',
        'views/reportes.xml',
        'views/clientes.xml',
        'views/users.xml',
        'views/pagos.xml',
        'views/calidad.xml',
        'views/comision.xml',
        'reports/etiquetas.xml',
        'reports/etiquetas_template.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}