# Reject Loan In

> **Module:** ssi_loan
>
> **Model:** `loan.in`
>
> **Menu:** Loan > Loans In
>
> **Actor:** user registered as an active approver on the record's approval flow
>
> **State:** `confirm` → `reject`
>
> **Requires:** `04-confirm`

## Pre-Condition

- **Record:** Record is in **Waiting for Approval** status.
- **Access:** User is registered as an active approver on the record's approval flow.

## Flow

1. Open the **Loan > Loans In** menu.
2. Open the record to reject.
3. Click the **Reject** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Rejected**.
