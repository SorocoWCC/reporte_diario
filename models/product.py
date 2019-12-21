# -*- coding: utf-8 -*-

from odoo import models, fields, api

class product(models.Model):
    _name = 'product.template'
    _inherit = 'product.template'
    precio_venta_reporte = fields.Float(string = 'Precio de Venta Reporte Diario:')
    incluir_reporte = fields.Boolean(string = 'Incluir en Reporte Diario:', default=False)

	