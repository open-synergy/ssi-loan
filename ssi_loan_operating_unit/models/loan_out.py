# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class LoanOut(models.Model):  # pylint: disable=too-few-public-methods
    """
    Ties each outgoing loan document to a single operating unit.

    Adds ``mixin.single_operating_unit`` so every ``loan.out`` record
    carries an ``operating_unit_id``. As a result, the list of
    outgoing loans a user sees is filtered by operating unit through
    this module's record rule.
    """

    _name = "loan.out"
    _inherit = [
        "loan.out",
        "mixin.single_operating_unit",
    ]
