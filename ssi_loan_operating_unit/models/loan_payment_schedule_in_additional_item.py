# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class LoanPaymentScheduleInAdditionalItem(models.Model):
    # Propagates the operating unit of the originating loan to the
    # journal entry booked for an additional item of a schedule row.

    _name = "loan.payment_schedule_in_additional_item"
    _inherit = ["loan.payment_schedule_in_additional_item"]

    def _prepare_account_move(self):
        """Build the entry header with the originating loan's OU.

        :return: dict of ``account.move`` values
        """
        self.ensure_one()
        res = super()._prepare_account_move()
        res["operating_unit_id"] = self.schedule_id.loan_id.operating_unit_id.id
        return res

    def _prepare_ml(self, move, *args, **kwargs):
        """Build the entry line values with the originating loan's OU.

        :param move: the ``account.move`` the line will belong to
        :return: dict of ``account.move.line`` values
        """
        self.ensure_one()
        res = super()._prepare_ml(move, *args, **kwargs)
        res["operating_unit_id"] = self.schedule_id.loan_id.operating_unit_id.id
        return res
