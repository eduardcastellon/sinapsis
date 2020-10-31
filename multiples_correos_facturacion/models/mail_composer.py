# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import base64
import re

from odoo import _, api, fields, models, SUPERUSER_ID, tools
from odoo.tools.safe_eval import safe_eval
from odoo.exceptions import UserError


class MailComposer(models.TransientModel):
    _inherit = ['mail.compose.message']

    # partner_ids = fields.Char(string='Emails de faturación', required=False)
    #     partner_ids = fields.Many2many(
    #         'res.partner', 'mail_compose_message_res_partner_rel',
    #         'wizard_id', 'partner_id', 'Additional Contacts')

    #     @api.model
    #     def default_get(self, fields):
    #         res = super(MailComposer, self).default_get(fields)
    #         raise UserError(_(res))
    #         partner = self.env['res.partner'].search([('id','=', 616)])
    #         res['partner_ids'] = [partner.id]
    #         return res

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

# class AccountInvoiceSend(models.TransientModel):
#     _inherit = ['account.invoice.send']

#     @api.model
#     def send_and_print_action(self):
#         res = super(AccountInvoiceSend, self).send_and_print_action()

#         raise UserError(_(res))

# class Message(models.Model):
#     _inherit = ['mail.message']

#     def write(self, vals):
#         partner = self.env['res.partner'].search([('id','=', 616)])
#         vals['notified_partner_ids'] = partner.id
#         res = super(Message, self).write(vals)
# #         raise UserError(_(vals.notified_partner_ids))
# #         self.notified_partner_ids = [616]
# #         res = super(Message, self).default_get(fields)
# #         raise UserError(_(res))
# #         res['partner_ids'] = [partner.id]

#         return res
