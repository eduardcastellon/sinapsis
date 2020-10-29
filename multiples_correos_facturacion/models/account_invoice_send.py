# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class AccountInvoiceSend(models.TransientModel):
    _inherit = ['account.invoice.send']

    partner_ids = fields.Char(string='Emails de faturación', required=False)
