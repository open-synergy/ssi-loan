# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class LoanPaymentScheduleOut(models.Model):  # pylint: disable=too-few-public-methods
    """
    Propagates the operating unit of the parent loan to the journal
    entries created from a payment schedule row (principal
    receivable/payable and interest realization).
    """

    _name = "loan.payment_schedule_out"
    _inherit = ["loan.payment_schedule_out"]

    def _prepare_principle_receivable_move_line(self, move):
        """Build the principal line with the parent loan's OU.

        :param move: the ``account.move`` the line will belong to
        :return: dict of ``account.move.line`` values
        """
        self.ensure_one()
        res = super()._prepare_principle_receivable_move_line(move)
        res["operating_unit_id"] = self.loan_id.operating_unit_id.id
        return res

    def _prepare_interest_realization_move(self):
        """Build the interest move header with the parent loan's OU.

        :return: dict of ``account.move`` values
        """
        self.ensure_one()
        res = super()._prepare_interest_realization_move()
        res["operating_unit_id"] = self.loan_id.operating_unit_id.id
        return res

    def _prepare_interest_realization_move_line(self, move):
        """Build the interest receivable line with the parent loan's OU.

        :param move: the ``account.move`` the line will belong to
        :return: dict of ``account.move.line`` values
        """
        self.ensure_one()
        res = super()._prepare_interest_realization_move_line(move)
        res["operating_unit_id"] = self.loan_id.operating_unit_id.id
        return res

    def _prepare_interest_income_move_line(self, move):
        """Build the interest income line with the parent loan's OU.

        :param move: the ``account.move`` the line will belong to
        :return: dict of ``account.move.line`` values
        """
        self.ensure_one()
        res = super()._prepare_interest_income_move_line(move)
        res["operating_unit_id"] = self.loan_id.operating_unit_id.id
        return res
