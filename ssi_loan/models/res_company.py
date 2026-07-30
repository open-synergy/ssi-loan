# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class ResCompany(models.Model):
    """Enable ``res.company`` to carry ``ssi_loan`` settings fields.

    Pure ``_inherit`` hook so ``abstract.config.settings`` (from
    ``configuration_helper``) can mirror any ``setting_``-prefixed
    company field of this module onto ``res.config.settings``. No
    such field is defined yet: loan defaults currently live directly
    on ``loan.type`` as ``company_dependent`` fields instead.
    """

    _name = "res.company"
    _inherit = "res.company"
