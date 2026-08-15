# Deactivate Loan Collateral Type

> **Module:** ssi_loan
> **Model:** `loan_collateral_type`
> **Menu:** Loan > Configuration > Loan Collateral Types
> **Actor:** user in group *Loan Collateral Type* (`loan_collateral_type_group`)
> **Active:** `true` → `false`
> **Requires:** `01-create`

## Pre-Condition

- **Access:** User must belong to the **Loan Collateral Type** access group
  (`loan_collateral_type_group`).

## Flow

1. Open the **Loan > Configuration > Loan Collateral Types** menu.
2. Select one or more records to deactivate (check the checkbox).
3. Click **Action** > **Archive**.
4. Click **OK** to confirm.

## Post-Condition

- The records are archived and no longer appear in the default list view.
- Deactivated records cannot be selected on new loan collateral lines.
- Transactions that already use this record can still be viewed.
