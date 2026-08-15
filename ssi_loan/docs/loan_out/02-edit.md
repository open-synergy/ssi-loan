# Edit Loan Out

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
- **Access:** User must belong to the **User** access group (`loan_out_user_group`).

## Flow

1. Open the **Loan > Loans Out** menu.
2. Find and open the record to edit.
3. Change the required fields.
4. Click **Save**.

## Post-Condition

- The record is updated with the new values.
