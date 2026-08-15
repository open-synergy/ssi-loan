# Unmark Principle as Manual — Loan Out

> **Module:** ssi_loan
> **Model:** `loan.out`
> **Menu:** Loan > Loans Out
> **Actor:** user in group *User* (`loan_out_user_group`)
> **Requires:** `15-mark-principle-as-manual`

## Pre-Condition

- **Record:** Record is in **Draft** status.
- **Record:** The **Payment Schedule** line's **Principle Payment State** is **Manually
  Control**.
- **Access:** User must belong to the **User** access group (`loan_out_user_group`).

## Flow

1. Open the **Loan > Loans Out** menu.
2. Open the record.
3. Open the **Repayment Term** tab.
4. In the **Payment Schedule** table, click the icon button (tooltip: **Unmark as
   Manually Control**) on the line to unmark.

## Post-Condition

- The line's **Principle Payment State** changes to **Unpaid**.
- The line's principal amount is included back in **Total Principle Amount** instead of
  **Total Manual Principle Amount**.
