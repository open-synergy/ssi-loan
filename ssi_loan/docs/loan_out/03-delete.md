# Delete Loan Out

> **Module:** ssi_loan
>
> **Model:** `loan.out`
>
> **Menu:** Loan > Loans Out
>
> **Actor:** user in group _User_ (`loan_out_user_group`)
>
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Record is in **Draft** status.
- **Record:** Document number is still **/** (not yet generated).
- **Access:** User must belong to the **User** access group (`loan_out_user_group`).

## Flow

1. Open the **Loan > Loans Out** menu.
2. Open the record to delete.
3. Click **Action** > **Delete**.
4. Click **OK** to confirm.

## Post-Condition

- The record is permanently removed from the system.
