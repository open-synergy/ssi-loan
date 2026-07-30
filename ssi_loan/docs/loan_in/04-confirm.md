# Confirm Loan In

## Pre-Condition

- Record is in **Draft** status.
- **Total Principle Amount** (the sum of the **Payment Schedule** lines, built with the
  **Payment Schedule** button) equals **Loan Amount**.
- **Loan Amount** does not exceed the loan type's **Maximum Loan Amount**.
- User must belong to the **User** access group (`loan_in_user_group`).

## Flow

1. Open the **Loan > Loans In** menu.
2. Open the record to confirm.
3. Click the **Confirm** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Waiting for Approval**.
