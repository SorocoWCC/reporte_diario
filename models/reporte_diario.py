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
        return str(datetime.now(timezone('America/Costa_Rica')).strftime("%Y-%m-%d"))

    _inherit = 'mail.thread'
    _name = 'reporte_diario'

    name = fields.Date(string='Fecha', default=_get_name, copy=False, readonly=True)
    resumen_producto_ids = fields.One2many(comodel_name='resumen_producto', inverse_name='reporte_id', string="Resumen Productos")
    state = fields.Selection ([('en_proceso','En proceso'), ('cerrado','Cerrado')], string='Estado', default='en_proceso', readonly=True)

    # Crea el reporte del dia
    @api.multi
    def action_crear_reporte(self):
        if not self.env['reporte_diario'].search([('name', '=', str(datetime.now(timezone('America/Costa_Rica')).strftime("%Y-%m-%d")) )]) :

            # Cerrar reportes anteriores
            reporte_anterior = self.env['reporte_diario'].search([('state', '=', 'en_proceso' )])
            if reporte_anterior :
                reporte_anterior.state  = 'cerrado'


            reporte_diario = self.env['reporte_diario'].create({'name':str(datetime.now(timezone('America/Costa_Rica')).strftime("%Y-%m-%d"))})

            for producto in self.env['product.template'].search([('incluir_reporte', '=', True )]) :
                reporte_diario.resumen_producto_ids.create({'product_id': producto.id, 'reporte_id': reporte_diario.id, 'precio_venta': producto.precio_venta_reporte}) 
                
    # Crea el reporte del dia
    @api.multi
    def action_actualizar_reporte(self):

        resumen_productos_dict={}
        reporte_diario = self.env['reporte_diario'].search([('state', '=', 'en_proceso')])
        for resumen in reporte_diario.resumen_producto_ids :
            resumen_productos_dict[str(resumen.product_id.id)] = {"nombre": str(resumen.product_id.name), "cantidad":resumen.cantidad, "precio_compra": resumen.precio_compra,
            "precio_venta": resumen.precio_venta, "inversion": resumen.inversion, "ganancia": resumen.ganancia}

        for orden_compra in reporte_diario.env['purchase.order'].search([('pago_caja', '=', 'pagado'), ('incluido_en_reporte', '=', False), ('fecha_pago', '>', str(reporte_diario.name) + " 00:00:00"),
                                     ('fecha_pago', '<=', str(reporte_diario.name) + " 23:59:59")]) :
            print(orden_compra.name)
            print(orden_compra.incluido_en_reporte)
            for linea_compra in orden_compra.order_line:

                if str(linea_compra.product_id.id) in resumen_productos_dict:
                    temp_dict = resumen_productos_dict[str(linea_compra.product_id.id)]
                    # Cantidad
                    temp_dict["cantidad"] = temp_dict["cantidad"] + linea_compra.product_qty
                    print("Inversion:" + str(temp_dict["inversion"]) + " SubTotal: " + str(linea_compra.price_subtotal) )
                    temp_dict["inversion"] = temp_dict["inversion"] + linea_compra.price_subtotal
                    print("La inversion es:" + str(temp_dict["inversion"]))
                    temp_dict["precio_compra"] = temp_dict["inversion"] / temp_dict["cantidad"]
                    temp_dict["ganancia"] = (temp_dict["cantidad"] * temp_dict["precio_venta"] - temp_dict["inversion"] )

                    resumen_productos_dict[str(linea_compra.product_id.id)] = temp_dict
                    print(resumen_productos_dict)

            orden_compra.incluido_en_reporte = True 
  
                    
        for resumen_producto in reporte_diario.resumen_producto_ids:
            temp_dict = resumen_productos_dict[str(resumen_producto.product_id.id)]
            resumen_producto.cantidad = temp_dict["cantidad"]
            resumen_producto.precio_compra = temp_dict["precio_compra"]
            resumen_producto.inversion = temp_dict["inversion"]
            resumen_producto.ganancia = temp_dict["ganancia"]

               
    # Crear Cronjobs
    @api.model
    def action_cronjobs(self):
        if not self.env['ir.cron'].search([('name', '=', 'Crear Reporte Diario')]):
            modelo = self.env['ir.model'].search([('name', '=', 'reporte_diario')])
            self.env['ir.cron'].create({'name':'Crear Reporte Diario', 'model_id': modelo.id,
                                        'state': 'code', 'code': 'model.action_crear_reporte()',
                                        'interval_number': 1, 'interval_type': 'hours', 'active': True, 
                                        'numbercall': '-1'})

        if not self.env['ir.cron'].search([('name', '=', 'Actualizar Reporte Diario')]):
            modelo = self.env['ir.model'].search([('name', '=', 'reporte_diario')])
            self.env['ir.cron'].create({'name':'Actualizar Reporte Diario', 'model_id': modelo.id,
                                        'state': 'code', 'code': 'model.action_actualizar_reporte()',
                                        'interval_number': 10, 'interval_type': 'minutes', 'active': True, 
                                        'numbercall': '-1'})    