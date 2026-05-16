# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class LoanOut(models.Model):
    _name = "loan.out"
    _inherit = [
        "loan.out",
        "mixin.documenso_signing_approval",
    ]

    _documenso_signing_create_page = True
