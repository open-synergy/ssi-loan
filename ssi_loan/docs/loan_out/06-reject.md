# Reject Loan Out

> **Module:** ssi_loan
> **Model:** `loan.out`
> **Menu:** Loan > Loans Out
> **Actor:** user registered as an active approver on the record's approval flow
> **State:** `confirm` → `reject`
> **Requires:** `04-confirm`

## Pre-Condition

- **Record:** Record is in **Waiting for Approval** status.
- **Access:** User is registered as an active approver on the record's approval flow.

## Flow

1. Open the **Loan > Loans Out** menu.
2. Open the record to reject.
3. Click the **Reject** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Rejected**.
