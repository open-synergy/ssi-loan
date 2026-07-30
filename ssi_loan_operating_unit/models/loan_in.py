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
