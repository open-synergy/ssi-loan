# Cancel Loan In

## Pre-Condition

- **Record:** Record is in **Draft**, **Waiting for Approval**, or **Ready to Process**
  status.
- **Record:** Record is not yet **Realized**, has no realized interest, and has no
  partially or fully paid principal/interest on any **Payment Schedule** line.
- **Access:** User must belong to the **Validator** access group
  (`loan_in_validator_group`).

## Flow

1. Open the **Loan > Loans In** menu.
2. Open the record to cancel.
3. Click the **Cancel** button.
4. In the **Select Cancel Reason** wizard, select the **Cancellation Reason**.
5. Click **Confirm**.

## Post-Condition

- Status changes to **Cancelled**.
