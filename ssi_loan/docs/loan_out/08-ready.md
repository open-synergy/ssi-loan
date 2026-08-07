# Set Ready Loan Out

This transition is not triggered by a button; it is executed automatically by the system
(`base.automation`) once the trigger condition below is met. The initial **Waiting for
Approval** → **Ready to Process** transition is triggered instead by the approval
mechanism — see the Post-Condition of `05-approve.md`.

## Pre-Condition

- **Record:** Record is in **In Progress** status.
- **Access:** No dedicated access right is required for the automatic transition itself;
  the user only needs their normal Accounting access to perform the reconciliation
  described below.

## Flow

1. Open the **Loan > Loans Out** menu.
2. Open the loan record.
3. Undo the reconciliation of the realization journal entry's header line so that the
   record's **Realized** field (**Accounting** tab) becomes unchecked. The system
   automatically transitions the record's status back to **Ready to Process**.

## Post-Condition

- Status changes to **Ready to Process**.
