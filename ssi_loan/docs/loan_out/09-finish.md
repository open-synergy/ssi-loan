# Finish Loan Out

> **Module:** ssi_loan
> **Model:** `loan.out`
> **Menu:** Loan > Loans Out
> **Actor:** system (`base.automation`) — user only needs standard Accounting access to perform the reconciliation described in Flow
> **State:** `open` → `done`
> **Requires:** `07-start`

This transition is not triggered by a button; it is executed automatically by the system
(`base.automation`) once the trigger condition below is met.

## Pre-Condition

- **Record:** Record is in **In Progress** status.
- **Access:** No dedicated access right is required for the automatic transition itself;
  the user only needs their normal Accounting access to perform the reconciliation
  described below.

## Flow

1. Open the **Loan > Loans Out** menu.
2. Open the loan record.
3. Reconcile the principal move line — and the interest move line, for lines that carry
   interest — of every remaining **Payment Schedule** line against the corresponding
   payments, until every line's **Principle Payment State** and (when applicable)
   **Interest Payment State** is **Paid** or **Manually Control**. The system
   automatically transitions the record's status to **Done** once the record's **Paid**
   field (**Accounting** tab) becomes checked.

## Post-Condition

- Status changes to **Done**.
