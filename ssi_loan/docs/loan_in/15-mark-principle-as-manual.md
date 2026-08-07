# Mark Principle as Manual — Loan In

## Pre-Condition

- **Record:** Record is in **Draft** status.
- **Record:** The **Payment Schedule** line's **Principle Payment State** is not already
  **Manually Control**.
- **Access:** User must belong to the **User** access group (`loan_in_user_group`).

## Flow

1. Open the **Loan > Loans In** menu.
2. Open the record.
3. Open the **Repayment Term** tab.
4. In the **Payment Schedule** table, click the icon button (tooltip: **Mark as Manually
   Control**) on the line to mark.

## Post-Condition

- The line's **Principle Payment State** changes to **Manually Control**.
- The line's principal amount is excluded from **Total Principle Amount** and included
  in **Total Manual Principle Amount** instead.
