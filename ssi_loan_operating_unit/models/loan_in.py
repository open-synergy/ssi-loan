# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class LoanIn(models.Model):  # pylint: disable=too-few-public-methods
    """
    Ties each incoming loan document to a single operating unit.

    Adds ``mixin.single_operating_unit`` so every ``loan.in`` record
    carries an ``operating_unit_id``. As a result, the list of
    incoming loans a user sees is filtered by operating unit through
    this module's record rule.
    """

    _name = "loan.in"
    _inherit = [
        "loan.in",
        "mixin.single_operating_unit",
    ]

    def _prepare_realization_move(self):
        """Build the realization move header with the loan's OU.

        Adds ``operating_unit_id`` so the realization entry is booked
        in the operating unit of this loan, not the triggering user's.

        :return: dict of ``account.move`` values
        """
        self.ensure_one()
        res = super()._prepare_realization_move()
        res["operating_unit_id"] = self.operating_unit_id.id
        return res

    def _prepare_header_move_line(self, move):
        """Build the realization header line with the loan's OU.

        :param move: the ``account.move`` the line will belong to
        :return: dict of ``account.move.line`` values
        """
        self.ensure_one()
        res = super()._prepare_header_move_line(move)
        res["operating_unit_id"] = self.operating_unit_id.id
        return res

    def _prepare_rounding_move_line(self, move, amount):
        """Build the rounding line with the loan's OU.

        :param move: the ``account.move`` the line will belong to
        :param amount: the debit-minus-credit difference to absorb
        :return: dict of ``account.move.line`` values
        """
        self.ensure_one()
        res = super()._prepare_rounding_move_line(move, amount)
        res["operating_unit_id"] = self.operating_unit_id.id
        return res
