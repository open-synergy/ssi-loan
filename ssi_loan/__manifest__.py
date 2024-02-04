# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Loan",
    "version": "14.0.1.6.0",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "application": True,
    "depends": [
        "ssi_master_data_mixin",
        "ssi_transaction_confirm_mixin",
        "ssi_transaction_ready_mixin",
        "ssi_transaction_open_mixin",
        "ssi_transaction_done_mixin",
        "ssi_transaction_cancel_mixin",
        "ssi_currency_mixin",
        "account",
        "base_automation",
        "configuration_helper",
        "ssi_decorator",
    ],
    "data": [
        "security/ir_module_category_data.xml",
        "security/res_group_data.xml",
        "security/ir.model.access.csv",
        "security/ir_rule_data.xml",
        "data/ir_sequence_data.xml",
        "data/sequence_template_data.xml",
        "data/policy_template_data.xml",
        "data/approval_template_data.xml",
        "data/ir_actions_server_data.xml",
        "data/base_automation_data.xml",
        "menu.xml",
        "views/res_config_settings_views.xml",
        "views/loan_type_views.xml",
        "views/loan_collateral_type_views.xml",
        "views/loan_additional_item_views.xml",
        "views/loan_mixin_views.xml",
        "views/loan_out_views.xml",
        "views/loan_in_views.xml",
    ],
    "demo": [
        "demo/account_account_demo.xml",
        "demo/account_journal_demo.xml",
        "demo/loan_type_demo.xml",
    ],
}
