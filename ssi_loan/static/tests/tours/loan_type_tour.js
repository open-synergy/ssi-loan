odoo.define("ssi_loan.loan_type_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // IK: docs/loan_type/01-create.md
    tour.register(
        "ssi_loan_loan_type_create",
        {
            test: true,
            url: "/web",
        },
        [
            // ── Flow 1 — Open the Loan > Configuration > Loan Types menu
            tour.stepUtils.showAppsMenuItem(),
            {
                content: "Open the Loan app",
                trigger: '.o_app[data-menu-xmlid="ssi_loan.menu_root_loan"]',
            },
            {
                content: "Open the Configuration menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_loan.menu_loan_configuration"]',
            },
            {
                content: "Open the Loan Types menu",
                trigger: '.o_menu_sections [data-menu-xmlid="ssi_loan.loan_type_menu"]',
            },
            {
                // Gate: wait for the TARGET action to be mounted, not just
                // any list view (the app may land on a stale list first).
                content: "Loan Types list is displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(Loan Types)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },

            // ── Flow 2 — Click the Create button
            {
                content: "Click Create",
                trigger: ".o_list_button_add",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Form is open in edit mode",
                trigger: ".o_form_view.o_form_editable",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },

            // ── Flow 3 — Fill in the required fields (Loan Type, Code,
            // Direction, Currency)
            {
                content: "Fill in the Loan Type name",
                trigger: ".o_field_widget[name='name']",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text Tour Loan Type",
            },
            {
                content: "Fill in Code",
                trigger: ".o_field_widget[name='code']",
                run: "text /",
            },
            {
                content: "Select the Direction",
                trigger: ".o_field_widget[name='direction'] select",
                run: "text Out",
            },
            {
                content: "Select the Currency",
                trigger: ".o_field_many2one[name='currency_id'] input",
                run: "text USD",
            },
            {
                content: "Pick the currency from the dropdown",
                trigger: ".ui-autocomplete .ui-menu-item a:contains(USD)",
                in_modal: false,
            },

            // ── Flow 4 — Open the Loan Configuration tab and fill in the
            // interest method and maximum loan amount
            {
                content: "Open the Loan Configuration tab",
                trigger: ".o_notebook .nav-link:contains(Loan Configuration)",
            },
            {
                content: "Select the Interest Method",
                trigger: ".o_field_widget[name='interest_method'] select",
                run: "text Flat",
            },
            {
                content: "Fill in the Maximum Loan Amount",
                trigger: ".o_field_widget[name='maximum_loan_amount']",
                run: "text 100000000",
            },

            // ── Flow 5 — Open the Accounting tab (accounts/journals are
            // optional, left blank)
            {
                content: "Open the Accounting tab",
                trigger: ".o_notebook .nav-link:contains(Accounting)",
            },
            {
                content: "Accounting tab is displayed",
                trigger: ".o_field_widget[name='realization_journal_id']",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },

            // ── Flow 6 — Open the Additional Item tab (no items available
            // for a brand-new type, left blank)
            {
                content: "Open the Additional Item tab",
                trigger: ".o_notebook .nav-link:contains(Additional Item)",
            },
            {
                content: "Additional Item tab is displayed",
                trigger: ".o_field_x2many[name='additional_item_ids']",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },

            // ── Flow 7 — Click Save
            {
                content: "Save the record",
                trigger: ".o_form_button_save",
            },

            // ── Post-Condition — A new record is created and is active
            // by default
            {
                content: "Loan Type record is saved and active",
                trigger:
                    ".o_form_view.o_form_readonly:not(:has(.ribbon:visible:contains(Archived)))",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
        ]
    );
});
