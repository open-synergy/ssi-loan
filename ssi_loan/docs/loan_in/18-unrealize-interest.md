# Unrealize Interest — Loan In

> **Module:** ssi_loan
>
> **Model:** `loan.in`
>
> **Menu:** Loan > Loans In
>
> **Actor:** user in group _User_ (`loan_in_user_group`)
>
> **Requires:** `17-realize-interest`

## Pre-Condition

- **Record:** Record is in **In Progress** status.
- **Record:** The **Payment Schedule** line's **Interest Payment State** is **Unpaid**.
- **Access:** User must belong to the **User** access group (`loan_in_user_group`).

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
