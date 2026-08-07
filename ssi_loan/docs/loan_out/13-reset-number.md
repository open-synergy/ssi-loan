# Reset Document Number — Loan Out

## Pre-Condition

- **Record:** Record is in **Draft** status.
- **Access:** User must belong to the **Validator** access group
  (`loan_out_validator_group`).

## Flow

1. Open the **Loan > Loans Out** menu.
2. Open the record whose document number will be reset.
3. Click the **Reset Document Number** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Document number returns to **/**.
- The record will receive an automatic number when it transitions to the **Ready to
  Process** state, according to the sequence template configuration.
