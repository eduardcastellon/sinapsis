# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = ['res.partner']

    emails_facturacion = fields.Char(
        string='Emails de facturación',
        required=False)
