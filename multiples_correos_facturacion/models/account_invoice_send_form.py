# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class AccountInvoiceSendForm(models.TransientModel):
    _inherit = ['account.invoice.send.form']

    partner_ids = fields.Float(string='Emails de faturación', required=False)
