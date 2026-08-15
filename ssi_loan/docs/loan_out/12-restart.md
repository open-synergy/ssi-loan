# Restart Loan Out

> **Module:** ssi_loan
>
> **Model:** `loan.out`
>
> **Menu:** Loan > Loans Out
>
> **Actor:** user in group _Validator_ (`loan_out_validator_group`)
>
> **State:** `cancel`/`reject` → `draft`
>
> **Requires:** `10-cancel`

## Pre-Condition

- **Record:** Record is in **Cancelled** or **Rejected** status.
- **Access:** User must belong to the **Validator** access group
  (`loan_out_validator_group`).

## Flow

1. Open the **Loan > Loans Out** menu.
2. Open the record to restart.
3. Click the **Restart** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status returns to **Draft**.
