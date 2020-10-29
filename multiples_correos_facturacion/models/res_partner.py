# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import date

class ResPartner(models.Model):
    _inherit = ['res.partner']

    email_facturacion = fields.Boolean(string='Email de faturación', required=False)
