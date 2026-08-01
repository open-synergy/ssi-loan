odoo.define("ssi_loan.loan_additional_item_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // IK: docs/loan_additional_item/01-create.md
    tour.register(
        "ssi_loan_loan_additional_item_create",
        {
            test: true,
            url: "/web",
        },
        [
            // ── Flow 1 — Open the Loan > Configuration > Additional Items
            // menu
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
                content: "Open the Additional Items menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_loan.loan_additional_item_menu"]',
            },
            {
                // Gate: wait for the TARGET action to be mounted, not just
                // any list view (the app may land on a stale list first).
                // The action's own name ("Loan Additional Item") is what
                // ends up in the breadcrumb, not the menu label.
                content: "Loan Additional Item list is displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(Loan Additional Item)",
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

            // ── Flow 3 — Fill in the required fields (Loan Additional
            // Item, Code)
            {
                content: "Fill in the Loan Additional Item name",
                trigger: ".o_field_widget[name='name']",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text Tour Additional Item",
            },
            {
                content: "Fill in Code",
                trigger: ".o_field_widget[name='code']",
                run: "text /",
            },

            // ── Flow 4 — Select the direction(s) this additional item
            // applies to
            {
                content: "Check Available for Loan Out",
                trigger: ".o_field_widget[name='loan_out_ok'] input",
                run: "click",
            },

            // ── Flow 5 — Open the Loan Out Configuration tab (accounts/
            // journal are optional, left blank)
            {
                content: "Open the Loan Out Configuration tab",
                trigger: ".o_notebook .nav-link:contains(Loan Out Configuration)",
            },
            {
                content: "Loan Out Configuration tab is displayed",
                trigger: ".o_field_widget[name='receivable_journal_id']",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },

            // ── Flow 6 — Open the Loan In Configuration tab (accounts/
            // journal are optional, left blank)
            {
                content: "Open the Loan In Configuration tab",
                trigger: ".o_notebook .nav-link:contains(Loan In Configuration)",
            },
            {
                content: "Loan In Configuration tab is displayed",
                trigger: ".o_field_widget[name='payable_journal_id']",
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
                content: "Loan Additional Item record is saved and active",
                trigger:
                    ".o_form_view.o_form_readonly:not(:has(.ribbon:visible:contains(Archived)))",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
        ]
    );
});
