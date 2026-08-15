# Delete Loan In

> **Module:** ssi_loan
> **Model:** `loan.in`
> **Menu:** Loan > Loans In
> **Actor:** user in group *User* (`loan_in_user_group`)
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Record is in **Draft** status.
- **Record:** Document number is still **/** (not yet generated).
- **Access:** User must belong to the **User** access group (`loan_in_user_group`).

## Flow

1. Open the **Loan > Loans In** menu.
2. Select one or more records to delete (check the checkbox).
3. Click **Action** > **Delete**.
4. Click **OK** to confirm.

## Post-Condition

- The selected records are permanently removed from the system.
