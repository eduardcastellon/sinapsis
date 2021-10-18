# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from odoo import models, fields, api, exceptions, _

import logging
_logger = logging.getLogger(__name__)

DAYS_DELAYED = 7

class ProjectTask(models.Model):
    _inherit = 'project.task'

    next_thresold_reminder_date = fields.Datetime(string=_('Next Thresold Reminder Date'))

    def get_task_url(self):
        return '/web?#id='+str(self.id)+'&view_type=form&model='+str(self._name)+'&db='+str(self._cr.dbname)

    def send_thresold_reminder_date(self):
        template = self.env.ref('perso_sinapsis.mail_template_task_limit_reminder')
        template.send_mail(self.id)

    def _cron_send_reminder_for_task(self, max_percent):

        tickets = self.search([('stage_id.is_closed', '=', False), ('user_id', '!=', False), ('progress', '>=', max_percent), '|', ('next_thresold_reminder_date', '=', False), ('next_thresold_reminder_date', '<', datetime.now())])

        if tickets:
            for ticket in tickets:
                ticket.send_thresold_reminder_date()
                ticket.write({'next_thresold_reminder_date': (ticket.next_thresold_reminder_date or datetime.now()) + timedelta(days=DAYS_DELAYED)})

        return True