# Realize Interest — Loan Out

> **Module:** ssi_loan
> **Model:** `loan.out`
> **Menu:** Loan > Loans Out
> **Actor:** user in group *User* (`loan_out_user_group`)
> **Requires:** `07-start`

## Pre-Condition

- **Record:** Record is in **In Progress** status.
- **Record:** The **Payment Schedule** line's **Interest Payment State** is
  **Unrealized**.
- **Access:** User must belong to the **User** access group (`loan_out_user_group`).

## Flow

1. Open the **Loan > Loans Out** menu.
2. Open the record.
3. Open the **Repayment Term** tab.
4. In the **Payment Schedule** table, click the icon button (tooltip: **Realize
   Interest**) on the line.

## Post-Condition

- An interest realization journal entry is posted for the line's interest amount, and
  the entries for its additional items (if any) are posted as well.
- The line's **Interest Payment State** changes from **Unrealized** to **Unpaid**.
