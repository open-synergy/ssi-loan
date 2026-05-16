# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class LoanIn(models.Model):  # pylint: disable=too-few-public-methods
    _name = "loan.in"
    _inherit = [
        "loan.in",
        "mixin.single_operating_unit",
    ]
