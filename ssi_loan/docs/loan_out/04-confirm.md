# Confirm Loan Out

## Pre-Condition

- **Record:** Record is in **Draft** status.
- **Record:** **Total Principle Amount** (the sum of the **Payment Schedule** lines,
  built with the **Payment Schedule** button) equals **Loan Amount**.
- **Record:** **Loan Amount** does not exceed the loan type's **Maximum Loan Amount**.
- **Access:** User must belong to the **User** access group (`loan_out_user_group`).

## Flow

1. Open the **Loan > Loans Out** menu.
2. Open the record to confirm.
3. Click the **Confirm** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Waiting for Approval**.
