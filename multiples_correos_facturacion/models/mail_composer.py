# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import base64
import re

from odoo import _, api, fields, models, SUPERUSER_ID, tools
from odoo.tools.safe_eval import safe_eval
from odoo.exceptions import UserError


class Notification(models.Model):
    _inherit = ['mail.notification']

    @api.model_create_multi
    def create(self, vals_list):
        nuevos_valores_para_notificar = []
        if vals_list:
            for notification in vals_list:
                message_id = notification['mail_message_id']
                message = self.env['mail.message'].search([('id', '=', message_id)])
                if message:
                    if message.model == 'account.move':
                        invoice = self.env['account.move'].search([('id', '=', message.res_id)])
                        id_cliente = invoice.partner_id.id
                        is_company = invoice.partner_id.is_company

                        # raise UserError(_(is_company))

                        if notification['res_partner_id'] != id_cliente:
                            nuevos_valores_para_notificar.append(notification)
        res = super(Notification, self).create(nuevos_valores_para_notificar)
        return res


class Message(models.Model):
    _inherit = ['mail.message']

    @api.model_create_multi
    def create(self, values_list):
        res = super(Message, self).create(values_list)
        # res.write({'notified_partner_ids': [616]})
        return res


class MailThread(models.AbstractModel):
    _inherit = ['mail.thread']

    def _notify_thread(self, message, msg_vals=False, **kwargs):
        nuevos_argumentos = {'partners': [], 'chanels': []}

        res = super(MailThread, self)._notify_thread(message, msg_vals=False, **kwargs)

        if (message.model == 'account.move'):
            invoice = self.env['account.move'].search([('id', '=', message.res_id)])
            id_cliente = invoice.partner_id.id
            is_company = invoice.partner_id.is_company
            for receptor in res['partners']:
                if receptor['id'] != id_cliente:
                    nuevos_argumentos['partners'].append(receptor)
        res['partners'] = nuevos_argumentos
        return res


class AccountInvoiceSend(models.TransientModel):
    _inherit = ['account.invoice.send']

    # def send_and_print_action(self):
    # raise UserError(_(self.partner_ids))
    @api.model
    def default_get(self, fields):

        res = super(AccountInvoiceSend, self).default_get(fields)

        invoice_ids = res['invoice_ids']
        if invoice_ids:
            invoices = self.env['account.move'].browse(invoice_ids)
            for invoice in invoices:
                seguidores_finales = []
                id_cliente = invoice.partner_id.id
                is_company = invoice.partner_id.is_company
                if is_company == True:
                    seguidores = invoice.message_follower_ids
                    if seguidores:
                        for seguidor in seguidores:
                            if seguidor.partner_id.id != id_cliente:
                                seguidores_finales.append(seguidor.id)
                self.env['account.move'].search([('id', '=', invoice.id)]).write(
                    {'message_follower_ids': seguidores_finales})

        return res


class MailComposer(models.TransientModel):
    _inherit = ['mail.compose.message']

    def send_mail(self, auto_commit=False):
        destinatarios = []
        self.partner_ids = []

        invoices = self.env[self.model].browse(self.res_id)
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
        res = super(MailComposer, self).send_mail()

        return res
        # self.partner_ids = _obtener_destinatarios()
        # raise UserError(_(self.partner_ids))

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

    def _obtener_destinatarios(self, modelo_vigente):
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

            return destinatarios