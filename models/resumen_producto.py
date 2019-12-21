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


class resumen_producto(models.Model):
    _name = "resumen_producto"
    _description = "Resumen Producto"

    reporte_id = fields.Many2one(comodel_name='reporte_diario', string='Reporte', delegate=True)
    product_id = fields.Many2one(comodel_name='product.product', string='Producto')
    cantidad = fields.Float('Cantidad')
    precio_compra = fields.Float('Precio Compra')
    precio_venta = fields.Float('Previo Venta')
    inversion = fields.Float('Inversión')    
    ganancia = fields.Float('Ganacia')
