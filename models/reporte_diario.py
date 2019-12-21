# -*- coding: utf-8 -*-

import pytz 
from openerp import fields
from datetime import datetime
from datetime import timedelta  
from pytz import timezone 
from openerp import fields
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP
from openerp import models, fields, api
from openerp.exceptions import Warning
import time


class reporte_diario(models.Model):

    @api.model
    def _get_name(self):
        return str(str(fields.Date.today()) )

    _inherit = 'mail.thread'
    _name = 'reporte_diario'

    name = fields.Char(string='Name', default=_get_name, readonly=True, copy=False)
    resumen_producto_ids = fields.One2many(comodel_name='resumen_producto', inverse_name='reporte_id', string="Resumen Productos")

    # Crea el reporte del dia
    @api.multi
    def action_crear_reporte(self):
        if not self.env['reporte_diario'].search([('name', '=', str(fields.Date.today()) )]) :
            reporte_diario = self.env['reporte_diario'].create({'name':str(fields.Date.today())})

            for producto in self.env['product.template'].search([('incluir_reporte', '=', True )]) :
                print("================")
                print(producto.name)
                reporte_diario.resumen_producto_ids.create({'product_id': producto.id, 'reporte_id': reporte_diario.id}) 
                


    # Crear Cronjobs
    @api.model
    def action_cronjobs(self):
        if not self.env['ir.cron'].search([('name', '=', 'Crear Reporte Diario')]):
            modelo = self.env['ir.model'].search([('name', '=', 'reporte_diario')])
            self.env['ir.cron'].create({'name':'Crear Reporte Diario', 'model_id': modelo.id,
                                        'state': 'code', 'code': 'model.action_crear_reporte()',
                                        'interval_number': 1, 'interval_type': 'hours', 'active': True, 
                                        'numbercall': '-1'})                            