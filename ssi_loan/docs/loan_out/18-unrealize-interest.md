# Unrealize Interest — Loan Out

## Pre-Condition

- **Record:** Record is in **In Progress** status.
- **Record:** The **Payment Schedule** line's **Interest Payment State** is **Unpaid**.
- **Access:** User must belong to the **User** access group (`loan_out_user_group`).

## Flow

1. Open the **Loan > Loans Out** menu.
2. Open the record.
3. Open the **Repayment Term** tab.
4. In the **Payment Schedule** table, click the icon button (tooltip: **Unrealize
   Interest**) on the line.

## Post-Condition

- The line's interest realization journal entry and its additional item entries (if any)
  are deleted.
- The line's **Interest Payment State** changes back to **Unrealized**.
