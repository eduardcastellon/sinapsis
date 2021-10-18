# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from collections import OrderedDict
from dateutil.relativedelta import relativedelta
from operator import itemgetter

from odoo import fields, http, _
from odoo.http import request
from odoo.tools import date_utils, groupby as groupbyelem
from odoo.osv.expression import AND

from odoo.addons.portal.controllers.portal import pager as portal_pager
from odoo.addons.hr_timesheet.controllers.portal import TimesheetCustomerPortal


class TimesheetCustomerPortalRemove(TimesheetCustomerPortal):

    def _prepare_home_portal_values(self):
        values = super(TimesheetCustomerPortalRemove, self)._prepare_home_portal_values()
        values['timesheet_count'] = 0
        return values

    @http.route(['/my/timesheets', '/my/timesheets/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_timesheets(self, page=1, sortby=None, filterby=None, search=None, search_in='all', groupby='project', **kw):
        values = self._prepare_home_portal_values()
        return request.render("portal.portal_my_home", values)
