# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class AccountInvoiceSend(models.TransientModel):
    _inherit = ['account.invoice.send']

    @api.model
    def default_get(self, fields):
        res = super(AccountInvoiceSend, self).default_get(fields)
        res.update({
            'partner_ids': {}
        })
        return res