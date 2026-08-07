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

    // IK: docs/loan_additional_item/02-edit.md
    tour.register(
        "ssi_loan_loan_additional_item_edit",
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
                content: "Loan Additional Item list is displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(Loan Additional Item)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },

            // ── Flow 2 — Find and open the record to edit
            {
                content: "Open the record",
                trigger:
                    ".o_data_row:contains(TOUR Loan Additional Item Edit) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Form is open",
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
            {
                content: "Click the Edit button",
                trigger: ".o_form_button_edit",
            },
            {
                content: "Form is now editable",
                trigger: ".o_form_view.o_form_editable",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },

            // ── Flow 3 — Change the required fields
            {
                content: "Change the Loan Additional Item name",
                trigger: ".o_field_widget[name='name']",
                run: "text TOUR Loan Additional Item Edit Changed",
            },

            // ── Flow 4 — Click Save
            {
                content: "Save the record",
                trigger: ".o_form_button_save",
            },

            // ── Post-Condition — The record is updated with the new
            // values
            {
                content: "Record is saved with the new value",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(TOUR Loan Additional Item Edit Changed)",
                extra_trigger: ".o_form_view.o_form_readonly",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
        ]
    );

    // IK: docs/loan_additional_item/03-delete.md
    tour.register(
        "ssi_loan_loan_additional_item_delete",
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
                content: "Loan Additional Item list is displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(Loan Additional Item)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },

            // ── Flow 2 — Select one or more records to delete (check the
            // checkbox)
            {
                content: "Select the record's checkbox",
                trigger:
                    ".o_data_row:contains(TOUR Loan Additional Item Delete) .o_list_record_selector input",
                run: "click",
            },

            // ── Flow 3 — Click Action > Delete
            {
                content: "Open the Action menu",
                trigger: ".o_cp_action_menus button:contains(Action)",
            },
            {
                content: "Click Delete",
                trigger: ".o_cp_action_menus .o_menu_item a",
                run: function () {
                    var $delete = $(".o_cp_action_menus .o_menu_item a").filter(
                        function () {
                            return $(this).text().trim() === "Delete";
                        }
                    );
                    $delete[0].click();
                },
            },

            // ── Flow 4 — Click OK to confirm
            {
                content: "Confirm deletion",
                trigger: ".modal-footer button.btn-primary",
                in_modal: true,
            },

            // ── Post-Condition — The selected records are permanently
            // removed from the system
            {
                content: "Record no longer in the list",
                trigger:
                    ".o_list_view:not(:has(.o_data_row:contains(TOUR Loan Additional Item Delete)))",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
        ]
    );

    // IK: docs/loan_additional_item/04-deactivate.md
    tour.register(
        "ssi_loan_loan_additional_item_deactivate",
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
                content: "Loan Additional Item list is displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(Loan Additional Item)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },

            // ── Flow 2 — Select one or more records to deactivate (check
            // the checkbox)
            {
                content: "Select the record's checkbox",
                trigger:
                    ".o_data_row:contains(TOUR Loan Additional Item Deactivate) .o_list_record_selector input",
                run: "click",
            },

            // ── Flow 3 — Click Action > Archive
            {
                content: "Open the Action menu",
                trigger: ".o_cp_action_menus button:contains(Action)",
            },
            {
                content: "Click Archive",
                trigger: ".o_cp_action_menus .o_menu_item a",
                run: function () {
                    var $archive = $(".o_cp_action_menus .o_menu_item a").filter(
                        function () {
                            return $(this).text().trim() === "Archive";
                        }
                    );
                    $archive[0].click();
                },
            },

            // ── Flow 4 — Click OK to confirm
            {
                content: "Confirm archive",
                trigger: ".modal-footer button.btn-primary",
                in_modal: true,
            },

            // ── Post-Condition — The records are archived and no longer
            // appear in the default list view
            {
                content: "Record no longer in the default list",
                trigger:
                    ".o_list_view:not(:has(.o_data_row:contains(TOUR Loan Additional Item Deactivate)))",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
        ]
    );

    // IK: docs/loan_additional_item/05-activate.md
    tour.register(
        "ssi_loan_loan_additional_item_activate",
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
                content: "Loan Additional Item list is displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(Loan Additional Item)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },

            // ── Flow 2 — Enable the Archived filter in the search bar
            {
                content: "Wait for the list data to finish loading",
                trigger: ".o_list_view .o_data_row",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
            {
                content: "Open the Filters menu",
                trigger: ".o_filter_menu .o_dropdown_toggler_btn",
                run: function () {
                    this.$anchor[0].click();
                },
            },
            {
                content: "Enable the Archived filter",
                trigger: ".o_filter_menu .o_menu_item:contains(Archived) a",
                run: function () {
                    this.$anchor[0].click();
                },
            },

            // ── Flow 3 — Select one or more records to reactivate (check
            // the checkbox)
            {
                content: "Select the archived record's checkbox",
                trigger:
                    ".o_data_row:contains(TOUR Loan Additional Item Activate) .o_list_record_selector input",
                run: "click",
            },

            // ── Flow 4 — Click Action > Unarchive
            {
                content: "Open the Action menu",
                trigger: ".o_cp_action_menus button:contains(Action)",
            },
            {
                content: "Click Unarchive",
                trigger: ".o_cp_action_menus .o_menu_item a",
                run: function () {
                    var $unarchive = $(".o_cp_action_menus .o_menu_item a").filter(
                        function () {
                            return $(this).text().trim() === "Unarchive";
                        }
                    );
                    $unarchive[0].click();
                },
            },

            // ── Flow 5 — Click OK to confirm.
            // Odoo 14.0 core wraps ONLY "Archive" in Dialog.confirm
            // (list_controller.js _getActionMenuItems); "Unarchive"
            // calls _toggleArchiveState(false) directly with no dialog
            // at all. There is therefore no OK step to click here; the
            // IK's Flow 5 does not apply to this specific action in
            // this Odoo series (same verified deviation as
            // ssi_loan's loan_collateral_type_tour.js, tour
            // ssi_loan_loan_collateral_type_activate).
            //
            // Gate required (patterns.md §P): without it, the next step
            // (removing the Archived filter facet) races the still
            // in-flight action_unarchive RPC. The row is guaranteed
            // present in the Archived-filtered list before the button
            // is clicked, so once unarchive lands and the list
            // reloads, this row is guaranteed to leave it -- a valid
            // gate.
            {
                content: "Unarchive completes (row leaves the Archived list)",
                trigger:
                    ".o_list_view:not(:has(.o_data_row:contains(TOUR Loan Additional Item Activate)))",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },

            // ── Post-Condition — The records are restored and appear
            // again in the default list view
            {
                content: "Remove the Archived filter",
                trigger: ".o_searchview_facet .o_facet_remove",
                run: "click",
            },
            {
                content: "Record appears again in the default list",
                trigger: ".o_data_row:contains(TOUR Loan Additional Item Activate)",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
        ]
    );
});
