# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Loan + Operating Unit",
    "version": "14.0.1.0.2",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "contributors": [
        "Andhitia Rama <andhitia.r@gmail.com>",
    ],
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "ssi_loan",
        "ssi_operating_unit_mixin",
        "web_tour",
    ],
    "data": [
        "security/res_group/loan_out.xml",
        "security/res_group/loan_in.xml",
        "security/ir_rule/loan_out.xml",
        "security/ir_rule/loan_in.xml",
        "views/loan_out_views.xml",
        "views/loan_in_views.xml",
        "views/assets.xml",
    ],
}
