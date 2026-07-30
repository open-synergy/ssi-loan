# Start Loan In

This transition is not triggered by a button; it is executed automatically by the system
(`base.automation`) once the trigger condition below is met.

## Pre-Condition

- Record is in **Ready to Process** status, or in **Done** status.
- No dedicated access right is required for the automatic transition itself; the user
  only needs their normal Accounting access to perform the reconciliation described
  below.

## Flow

1. Open the **Loan > Loans In** menu.
2. Open the loan record.
3. If the record is in **Ready to Process**: reconcile the realization journal entry's
   header line (created when the loan became **Ready to Process**) against the
   received-fund payment or bank statement line in **Accounting**, so that the record's
   **Realized** field (**Accounting** tab) becomes checked. The system automatically
   transitions the record's status to **In Progress**.
4. If the record is in **Done**: undo the reconciliation of any payment schedule line's
   principal or interest so that at least one installment is no longer fully paid (the
   record's **Paid** field, **Accounting** tab, becomes unchecked). The system
   automatically returns the record's status to **In Progress**.

## Post-Condition

- Status changes to **In Progress**.
