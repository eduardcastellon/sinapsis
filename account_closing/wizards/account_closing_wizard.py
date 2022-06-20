# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

from .query_utils import PYG_QUERY, CLOSE_QUERY, OPEN_QUERY

import datetime
import logging
_logger = logging.getLogger(__name__)


class AccountClosingWizard(models.TransientModel):
    """"""
    _name = 'account.closing.wizard'
    _description = "Wizard: Account closure"

    def _default_user_id(self):
        """"""
        return self.env.uid

    def _default_company_id(self):
        """"""
        if self.company_id:
            return self.company_id
        else:
            return self.env.company[0]

    def _default_currency_id(self):
        """"""
        return self._default_company_id().currency_id[0]

    def _default_account_129(self):
        """"""
        return self.env["account.account"].sudo().search([
            ('code', 'ilike', '129%'),
            ('company_id', '=', self._default_company_id().id)])[0]

    def _default_domain_company_id(self):
        """"""
        user = self.env['res.users'].browse(self._default_user_id())
        companies = []
        companies.append(user.company_id.id)

        # Multi-company
        for company in user.company_ids:
            companies.append(company.id)

        return [('id', 'in', companies)]

    def _default_domain_currency_id(self):
        """"""
        return [('id', '=', self._default_currency_id().id)]

    def _default_domain_journal_id(self):
        """"""
        return [('company_id', '=', self._default_company_id().id)]

    def _default_domain_account_129(self):
        """"""
        return ['&',
            ('code', 'ilike', '129%'),
            ('company_id', '=', self._default_company_id().id)]

    company_id = fields.Many2one(
        'res.company', string=_("Company"), required=True,
        domain=_default_domain_company_id,
        default=_default_company_id)
    journal_id = fields.Many2one(
        'account.journal', string=_('Journal'), required=True,
        domain=_default_domain_journal_id)
    currency_id = fields.Many2one(
        'res.currency', string=_("Currency"), required=True,
        domain=_default_domain_currency_id,
        default=_default_currency_id)
    account_129 = fields.Many2one(
        'account.account', string=_("Results account"),
        domain=_default_domain_account_129,
        default=_default_account_129)
    is_PYG = fields.Boolean(string=_("Include PyG?"))
    start_date = fields.Date(string=_("Start date"), required=True)
    end_date = fields.Date(string=_("End date"), required=True)

    @api.constrains('start_date', 'end_date')
    def _check_date(self):
        """"""
        for r in self:
            if r.start_date >= r.end_date:
                raise ValidationError(_(
                    "Wrong date. Start date must be less than the end date."))

    # onchange handler
    @api.onchange('company_id')
    def _onchange_company(self):
        """"""
        self.currency_id = self._default_currency_id()
        self.account_129 = self._default_account_129()

        return {
            'domain': {
                'currency_id': self._default_domain_currency_id(),
                'account_129': self._default_domain_account_129(),
                'journal_id': self._default_domain_journal_id()
            }
        }

    def __get_new_move(self, currency_id, journal_id, date):
        """
            :param
                currency_id Currency record
                journal_id  Journal record
                date datetime.datetime.today().strftime('%Y-%m-%d')
        """
        return self.env['account.move'].sudo().create({
            'currency_id': currency_id.id,
            'date': date.strftime('%Y-%m-%d'),
            'extract_state': 'no_extract_requested',
            'journal_id': journal_id.id,
            'type': 'entry',  # Para 14.0 'move_type'
            'state': 'draft'
        })

    def create_closing(self):
        """"""
        account_move_pyg_condition = ''
        account_move_pyg = None

        if self.is_PYG:
            # PyG
            account_move_pyg = self.__get_new_move(
                self.currency_id, self.journal_id, self.end_date)
            account_move_pyg_condition = "or id = {}".format(
                account_move_pyg.id)

            pyg_q = PYG_QUERY.format(
                # Apuntes
                start_date=self.start_date,
                end_date=self.end_date,
                company_id=self._default_company_id().id,
                # Account 6% 7%
                move_id=account_move_pyg.id,
                date=self.end_date,
                account_129=self.account_129.id,
                reference="{} {}".format(
                    _("PyG"), self.end_date.strftime('%Y')))

            _logger.critical("PYG Q")
            _logger.critical(pyg_q)

            self.env.cr.execute(pyg_q)

            result_pyg = self.env.cr.rowcount
            

        # Close
        account_move_close = self.__get_new_move(
            self.currency_id, self.journal_id, self.end_date)

        c_q = CLOSE_QUERY.format(
            # Apuntes
            start_date=self.start_date,
            end_date=self.end_date,
            company_id=self._default_company_id().id,
            account_move_pyg_condition=account_move_pyg_condition,
            #
            move_id=account_move_close.id,
            date=self.end_date,
            reference="{} {}".format(
                _("Closing"), self.end_date.strftime('%Y')))

        _logger.critical("close query")
        _logger.critical(c_q)

        self.env.cr.execute(c_q)

        result_close = self.env.cr.rowcount
        
        # Open
        next_date = datetime.timedelta(days=1) + self.end_date
        account_move_open = self.__get_new_move(
            self.currency_id, self.journal_id, next_date)

        o_q = OPEN_QUERY.format(
            # Apuntes
            start_date=self.start_date,
            end_date=self.end_date,
            company_id=self._default_company_id().id,
            account_move_pyg_condition=account_move_pyg_condition,
            #
            move_id=account_move_open.id,
            date=next_date,
            reference="{} {}".format(
                _("Opening"), next_date.strftime('%Y')))

        _logger.critical("OPEN QUERY")
        _logger.critical(o_q)

        self.env.cr.execute(o_q)

        result_open = self.env.cr.rowcount
        
        if account_move_pyg:
            _logger.critical("AccountClosing PYG ({}): Rows affected {}".format(
                    account_move_pyg.id,
                    result_pyg))

        _logger.critical("AccountClosing Close({}): Rows affected {}".format(
            account_move_close.id,
            result_close))

        _logger.critical("AccountClosing Open({}): Rows affected {}".format(
            account_move_open.id,
            result_open))
