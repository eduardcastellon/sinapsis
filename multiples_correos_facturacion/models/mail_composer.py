# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import base64
import re

from odoo import _, api, fields, models, SUPERUSER_ID, tools
from odoo.tools.safe_eval import safe_eval
from odoo.exceptions import UserError


class AccountInvoiceSend(models.TransientModel):
    _inherit = ['account.invoice.send']

    partner_ids = fields.Many2many(
        'res.partner', 'mail_compose_message_res_partner_rel')

    @api.model
    def default_get(self, fields):
        destinatarios = []

        res = super(AccountInvoiceSend, self).default_get(fields)
        invoice_ids = res['invoice_ids']
        if invoice_ids:
            invoices = self.env['account.move'].browse(invoice_ids)
            for invoice in invoices:
                if (invoice.partner_id.email_facturacion == True):
                    destinatarios.append(invoice.partner_id.id)

                contactos_cliente = invoice.partner_id.child_ids
                if contactos_cliente:
                    for contacto in contactos_cliente:
                        if contacto.email_facturacion == True:
                            destinatarios.append(contacto.id)
        res['partner_ids'] = destinatarios

        raise UserError(_(res))

        return res


class MailComposer(models.TransientModel):
    _inherit = ['mail.compose.message']

    def get_mail_values(self, res_ids):
        destinatarios = []
        modelo_vigente = self.model

        if (modelo_vigente == 'account.move'):
            # Recuperamos los contactos que son para facturacion
            invoices = self.env[self.model].browse(res_ids)
            if invoices:
                for invoice in invoices:
                    if (invoice.partner_id.email_facturacion == True):
                        destinatarios.append(invoice.partner_id.id)

                    contactos_cliente = invoice.partner_id.child_ids
                    if contactos_cliente:
                        for contacto in contactos_cliente:
                            if contacto.email_facturacion == True:
                                destinatarios.append(contacto.id)

            self.partner_ids = destinatarios
        #             self.notified_partner_ids = destinatarios
        res = super(MailComposer, self).get_mail_values(res_ids)

        return res
