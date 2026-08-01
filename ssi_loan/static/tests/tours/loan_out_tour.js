odoo.define("ssi_loan.loan_out_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // ── Shared building block — Flow 1 of every loan.out IK: open the
    // Loan > Loans Out menu.
    var openLoanOutMenu = [
        tour.stepUtils.showAppsMenuItem(),
        {
            content: "Open the Loan app",
            trigger: '.o_app[data-menu-xmlid="ssi_loan.menu_root_loan"]',
        },
        {
            content: "Open the Loans Out menu",
            trigger: '.o_menu_sections [data-menu-xmlid="ssi_loan.loan_out_menu"]',
        },
        {
            // Gate: wait for the TARGET action to be mounted, not just
            // any list view (the app may land on a stale list first).
            content: "Loans Out list is displayed",
            trigger: ".o_control_panel .breadcrumb-item.active:contains(Loans Out)",
            extra_trigger: ".o_list_view",
            run: function () {
                // Assertion only; do not trigger the default click action.
            },
        },
    ];

    // IK: docs/loan_out/01-create.md
    tour.register(
        "ssi_loan_loan_out_create",
        {
            test: true,
            url: "/web",
        },
        [].concat(openLoanOutMenu, [
            // ── Flow 2 — Click the New button (14.0: "Create")
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

            // ── Flow 3 — Fill in the required fields
            {
                content: "Fill in Date Transaction",
                trigger: ".o_field_widget[name='date'] input",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text 01/15/2026",
            },
            {
                content: "Select the Partner",
                trigger: ".o_field_many2one[name='partner_id'] input",
                run: "text Tour Loan Out Create Partner",
            },
            {
                content: "Pick the partner from the dropdown",
                trigger:
                    ".ui-autocomplete .ui-menu-item a:contains(Tour Loan Out Create Partner)",
                in_modal: false,
            },
            {
                content: "Select the Loan Type",
                trigger: ".o_field_many2one[name='type_id'] input",
                run: "text Tour Loan Type Out",
            },
            {
                content: "Pick the loan type from the dropdown",
                trigger:
                    ".ui-autocomplete .ui-menu-item a:contains(Tour Loan Type Out)",
                in_modal: false,
            },
            {
                content: "Fill in the Loan Amount",
                trigger: ".o_field_widget[name='loan_amount'] input",
                run: "text 3000",
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
            {
                content: "Fill in the Loan Period",
                trigger: ".o_field_widget[name='manual_loan_period'] input",
                run: "text 6",
            },
            {
                content: "Fill in the First Payment Date",
                trigger: ".o_field_widget[name='first_payment_date'] input",
                run: "text 02/15/2026",
            },

            // ── Flow 4 — Optionally add lines in the Collaterals tab
            // (left blank; adding a line is not exercised here)
            {
                content: "Open the Collaterals tab",
                trigger: ".o_notebook .nav-link:contains(Collaterals)",
            },
            {
                content: "Collaterals tab is displayed",
                trigger: ".o_field_x2many[name='collateral_ids']",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },

            // ── Flow 5 — Click Save
            {
                content: "Save the record",
                trigger: ".o_form_button_save",
            },

            // ── Post-Condition — A new record is created in Draft status
            {
                content: "Record is saved",
                trigger: ".o_form_view.o_form_readonly",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
            {
                content: "Status is Draft",
                trigger:
                    ".o_statusbar_status .o_arrow_button[data-value='draft'].btn-primary",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
        ])
    );

    // IK: docs/loan_out/14-compute-payment-schedule.md
    tour.register(
        "ssi_loan_loan_out_compute_payment_schedule",
        {
            test: true,
            url: "/web",
        },
        [].concat(openLoanOutMenu, [
            // ── Flow 2 — Open the record
            {
                content: "Open the record",
                trigger:
                    ".o_data_row:contains(Tour Loan Out Schedule Partner) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Record form is displayed",
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },

            // ── Flow 3 — Open the Repayment Term tab
            {
                content: "Open the Repayment Term tab",
                trigger: ".o_notebook .nav-link:contains(Repayment Term)",
            },

            // ── Flow 4 — Click the Payment Schedule button
            {
                content: "Click the Payment Schedule button",
                trigger: "button[name='action_compute_payment']",
                extra_trigger: ".o_form_view",
            },

            // ── Post-Condition — Payment Schedule lines are rebuilt
            {
                content: "Payment Schedule lines are rendered",
                trigger: ".o_field_x2many[name='payment_schedule_ids'] .o_data_row",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
        ])
    );

    // IK: docs/loan_out/04-confirm.md
    tour.register(
        "ssi_loan_loan_out_confirm",
        {
            test: true,
            url: "/web",
        },
        [].concat(openLoanOutMenu, [
            // ── Flow 2 — Open the record to confirm
            {
                content: "Open the record",
                trigger:
                    ".o_data_row:contains(Tour Loan Out Confirm Partner) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Record form is displayed",
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },

            // ── Flow 3 — Click the Confirm button
            {
                content: "Click the Confirm button",
                trigger: ".o_statusbar_buttons button[name='action_confirm']",
                extra_trigger: ".o_form_view",
            },

            // ── Flow 4 — Click OK on the confirmation dialog
            {
                content: "Confirm the dialog",
                trigger: ".modal-footer button.btn-primary",
                in_modal: true,
            },

            // ── Post-Condition — Status changes to Waiting for Approval
            {
                content: "Status is Waiting for Approval",
                trigger:
                    ".o_statusbar_status .o_arrow_button[data-value='confirm'].btn-primary",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
        ])
    );

    // IK: docs/loan_out/05-approve.md
    tour.register(
        "ssi_loan_loan_out_approve",
        {
            test: true,
            url: "/web",
        },
        [].concat(openLoanOutMenu, [
            // ── Flow 2 — Open the record to approve
            {
                content: "Open the record",
                trigger:
                    ".o_data_row:contains(Tour Loan Out Approve Partner) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Record form is displayed",
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },

            // ── Flow 3 — Click the Approve button
            {
                content: "Click the Approve button",
                trigger: ".o_statusbar_buttons button[name='action_approve_approval']",
                extra_trigger: ".o_form_view",
            },

            // ── Flow 4 — Click OK on the confirmation dialog
            {
                content: "Confirm the dialog",
                trigger: ".modal-footer button.btn-primary",
                in_modal: true,
            },

            // ── Post-Condition — All approval levels are fulfilled, so
            // the status automatically changes to Ready to Process
            {
                content: "Status is Ready to Process",
                trigger:
                    ".o_statusbar_status .o_arrow_button[data-value='ready'].btn-primary",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
        ])
    );

    // IK: docs/loan_out/10-cancel.md
    tour.register(
        "ssi_loan_loan_out_cancel",
        {
            test: true,
            url: "/web",
        },
        [].concat(openLoanOutMenu, [
            // ── Flow 2 — Open the record to cancel
            {
                content: "Open the record",
                trigger:
                    ".o_data_row:contains(Tour Loan Out Cancel Partner) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Record form is displayed",
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },

            // ── Flow 3 — Click the Cancel button
            {
                content: "Click the Cancel button",
                trigger: ".o_statusbar_buttons button:enabled:contains(Cancel)",
                extra_trigger: ".o_form_view",
            },

            // ── Flow 4 — In the Select Cancel Reason wizard, select the
            // Cancellation Reason
            {
                // 14.0: do NOT prefix with `.modal` — the trigger is
                // searched INSIDE the visible modal already.
                content: "Wizard is open",
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
            {
                content: "Select the cancellation reason",
                trigger: "label:contains(Tour Cancel Reason)",
            },

            // ── Flow 5 — Click Confirm
            {
                content: "Confirm the wizard",
                trigger: ".modal-footer button[name='action_confirm']",
            },
            {
                // The wizard's Confirm button itself asks "Are you
                // sure?" — a second dialog stacked on top of the
                // wizard. `$modal_displayed` resolves to the topmost
                // visible modal, so this selector targets that one.
                content: "Confirm the dialog",
                trigger: ".modal-footer button.btn-primary",
                in_modal: true,
            },

            // ── Post-Condition — Status changes to Cancelled
            {
                content: "Status is Cancelled",
                trigger:
                    ".o_statusbar_status .o_arrow_button[data-value='cancel'].btn-primary",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
        ])
    );
});
