# Approve Loan Out

> **Module:** ssi_loan
> **Model:** `loan.out`
> **Menu:** Loan > Loans Out
> **Actor:** user registered as an active approver on the record's approval flow
> **State:** `confirm` → `ready`
> **Requires:** `04-confirm`

## Pre-Condition

- **Record:** Record is in **Waiting for Approval** status.
- **Access:** User is registered as an active approver on the record's approval flow.

## Flow

1. Open the **Loan > Loans Out** menu.
2. Open the record to approve.
3. Click the **Approve** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- If all approval levels are fulfilled, the loan realization journal entry is created
  and the status automatically changes to **Ready to Process** (triggered by the
  approval mechanism, not a separate button).
- If there are still pending approval levels, status remains **Waiting for Approval**.
