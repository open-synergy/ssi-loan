// Copyright 2026 OpenSynergy Indonesia
// Copyright 2026 PT. Simetri Sinergi Indonesia
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

odoo.define("ssi_loan_documenso_signing.loan_out_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // IK: docs/loan_out/05-approve.md (E2a delta -- Modified Flow)
    // Navigation (open menu -> open record) is retraced from the base IK
    // ssi_loan/docs/loan_out/05-approve.md Flow steps 1-2 -- see skill
    // odoo-development-ui-test, scope-and-boundaries.md §3 ("E2a --
    // telusur-ulang aksi itu dari base sampai titik ubah"). The delta
    // assertion, anchored at base Flow step 2 (open the record to
    // approve), verifies the Signature Requests tab injected because
    // `_documenso_signing_create_page = True`; this tab is always
    // present once this module is installed, regardless of whether
    // Documenso signing is actually used for the approval (Modified
    // Flow, bullet 1). The fixture's active Approval Template has no
    // Documenso Signing Template configured, so base Flow steps 3-4
    // (Approve / OK) apply unchanged, exactly as documented in
    // ssi_loan/docs/loan_out/05-approve.md and in this module's own
    // Modified Flow bullet 2 -- the tour therefore continues to
    // completion (Ready to Process) without contacting any external
    // Documenso server.
    tour.register(
        "ssi_loan_documenso_signing_loan_out_approve",
        {
            test: true,
            url: "/web",
        },
        [
            // ── Base Flow 1 — Open the Loan > Loans Out menu.
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
                // Gate: wait for the TARGET action to be mounted, not
                // just any list view (the app may land on a stale list
                // first).
                content: "Loans Out list is displayed",
                trigger: ".o_control_panel .breadcrumb-item.active:contains(Loans Out)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },

            // ── Base Flow 2 — Open the record to approve.
            {
                content: "Open the record",
                trigger:
                    ".o_data_row:contains(Tour Loan Out Documenso Approve Partner) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Record form is displayed",
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },

            // ── Delta assertion (anchor: base Flow step 2) — the
            // Signature Requests tab is present.
            {
                content: "Open the Signature Requests tab",
                trigger: ".o_notebook .nav-link:contains(Signature Requests)",
            },
            {
                // Anchored on the group label rather than the (empty)
                // `approval_signature_request_id` many2one widget itself
                // -- a many2one rendered with no value has no text node
                // inside its link, so it collapses to a zero-size box
                // and jQuery's `:visible` (offsetWidth/offsetHeight)
                // never matches it, hanging the tour until timeout. See
                // skill odoo-development-ui-test, patterns.md §O.
                content:
                    "Signature Requests tab shows the Approval Signing " +
                    "Request group",
                trigger: ".o_horizontal_separator:contains(Approval Signing Request)",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },

            // ── Base Flow 3 — Click the Approve button.
            {
                content: "Click the Approve button",
                trigger: ".o_statusbar_buttons button[name='action_approve_approval']",
                extra_trigger: ".o_form_view",
            },

            // ── Base Flow 4 — Click OK on the confirmation dialog.
            {
                content: "Confirm the dialog",
                trigger: ".modal-footer button.btn-primary",
                in_modal: true,
            },

            // ── Post-Condition — All approval levels are fulfilled, so
            // the status automatically changes to Ready to Process.
            {
                content: "Status is Ready to Process",
                trigger:
                    ".o_statusbar_status .o_arrow_button[data-value='ready'].btn-primary",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
        ]
    );
});
