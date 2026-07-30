# Unmark Principle as Manual — Loan In

## Pre-Condition

- Record is in **Draft** status.
- The **Payment Schedule** line's **Principle Payment State** is **Manually Control**.
- User must belong to the **User** access group (`loan_in_user_group`).

## Flow

1. Open the **Loan > Loans In** menu.
2. Open the record.
3. Open the **Repayment Term** tab.
4. In the **Payment Schedule** table, click the icon button (tooltip: **Unmark as
   Manually Control**) on the line to unmark.

## Post-Condition

- The line's **Principle Payment State** changes to **Unpaid**.
- The line's principal amount is included back in **Total Principle Amount** instead of
  **Total Manual Principle Amount**.
