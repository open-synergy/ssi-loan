# Unrealize Interest — Loan In

## Pre-Condition

- Record is in **In Progress** status.
- The **Payment Schedule** line's **Interest Payment State** is **Unpaid**.
- User must belong to the **User** access group (`loan_in_user_group`).

## Flow

1. Open the **Loan > Loans In** menu.
2. Open the record.
3. Open the **Repayment Term** tab.
4. In the **Payment Schedule** table, click the icon button (tooltip: **Unrealize
   Interest**) on the line.

## Post-Condition

- The line's interest realization journal entry and its additional item entries (if any)
  are deleted.
- The line's **Interest Payment State** changes back to **Unrealized**.
