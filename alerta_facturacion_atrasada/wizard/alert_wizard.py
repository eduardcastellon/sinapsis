# -*- coding: utf-8 -*-
from odoo import models, fields, api


class AlertWizard(models.TransientModel):
    _name = 'alert.wizard'
    _description = "Wizard factura emitida"

    alerta = fields.Char(
        string='Alerta',
        required=False)

    @api.model
    def default_get(self, default_fields):
        result = super(AlertWizard, self).default_get(default_fields)
        if self._context.get('invoice') != "":
            result['alerta'] = "La factura que quieres publicar tiene una fecha inferior a la última factura publicada: " + self._context.get(
                'invoice')
        return result
