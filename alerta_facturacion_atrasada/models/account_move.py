# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import RedirectWarning, UserError, ValidationError, AccessError


class AccountMove(models.Model):
    _inherit = ['account.move']

    def action_post(self):
        fecha_ultima_factura = False
        fecha_factura_actual = self.invoice_date
        ultima_factura_publicada = ""

        facturas = self.env["account.move"].search(
            [("state", "=", 'posted')], limit=1
        )
        if facturas:
            for factura in facturas:
                fecha_ultima_factura = factura.invoice_date
                ultima_factura_publicada = factura.name

        if fecha_ultima_factura != False:
            if fecha_factura_actual:
                if fecha_ultima_factura > fecha_factura_actual:
                    view = self.env.ref('alerta_facturacion_atrasada.alert_wizard_form')
                    return {'name': _('Aviso importante Interno'),
                            'view_type': 'form',
                            'view_mode': 'form',
                            'target': 'new',
                            'res_model': 'alert.wizard',
                            'view_id': view.id,
                            'views': [(view.id, 'form')],
                            'type': 'ir.actions.act_window',
                            'context': {'invoice': ultima_factura_publicada}
                            }
