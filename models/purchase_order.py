# -*- coding: utf-8 -*-

from odoo import models, fields, api
from openerp.exceptions import ValidationError
from odoo.exceptions import UserError
from openerp.exceptions import Warning
from openerp import models, fields, api
from datetime import datetime
from pytz import timezone 
from datetime import timedelta  
import subprocess
import time
import base64
from openerp.http import request

class purchase_order(models.Model):
    _name = 'purchase.order'
    _inherit = 'purchase.order'

    incluido_en_reporte = fields.Boolean(string="Incluido en el reporte diario", default=False, readonly=True, copy=False)

