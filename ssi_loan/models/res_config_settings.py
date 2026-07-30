# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class ResConfigSettings(models.TransientModel):
    """Register the "Loan" panel in the Settings app.

    Pure ``_inherit`` hook: adds ``ssi_loan`` as an
    ``abstract.config.settings`` participant so its Feature/
    Integration sections render under Settings (see
    ``res_config_settings_views.xml``). No configuration field is
    mirrored yet, since ``res.company`` defines none for this module.
    """

    _name = "res.config.settings"
    _inherit = [
        "res.config.settings",
        "abstract.config.settings",
    ]
