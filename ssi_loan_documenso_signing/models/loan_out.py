# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class LoanOut(models.Model):
    """Add a Documenso e-signature stage to the loan.out approval.

    Inheriting ``mixin.documenso_signing_approval`` replaces the
    manual multiple-approval step of disbursed loans with a single
    ``documenso.signature.request``: the document is approved once
    that request reaches ``signed``, and rejected if the request is
    cancelled. Setting ``_documenso_signing_create_page = True``
    makes the mixin inject the Documenso Signing tab into the
    ``loan.out`` form view.
    """

    _name = "loan.out"
    _inherit = [
        "loan.out",
        "mixin.documenso_signing_approval",
    ]

    _documenso_signing_create_page = True
