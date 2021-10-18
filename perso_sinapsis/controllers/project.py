# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo.http import request
from odoo.osv import expression

from odoo.addons.hr_timesheet.controllers.project import ProjectCustomerPortal


class ProjectCustomerPortalRemove(ProjectCustomerPortal):

    def _task_get_page_view_values(self, task, access_token, **kwargs):
        values = super(ProjectCustomerPortalRemove, self)._task_get_page_view_values(task, access_token, **kwargs)
        values['timesheets'] = []
        return values
