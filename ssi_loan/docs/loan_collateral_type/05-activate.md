# Activate Loan Collateral Type

> **Module:** ssi_loan
>
> **Model:** `loan_collateral_type`
>
> **Menu:** Loan > Configuration > Loan Collateral Types
>
> **Actor:** user in group _Loan Collateral Type_ (`loan_collateral_type_group`)
>
> **Active:** `false` → `true`
>
> **Requires:** `04-deactivate`

## Pre-Condition

- **Access:** User must belong to the **Loan Collateral Type** access group
  (`loan_collateral_type_group`).

## Flow

1. Open the **Loan > Configuration > Loan Collateral Types** menu.
2. Enable the **Archived** filter in the search bar.
3. Select one or more records to reactivate (check the checkbox).
4. Click **Action** > **Unarchive**.
5. Click **OK** to confirm.

## Post-Condition

- The records are restored and appear again in the default list view.
- The records can be selected again on new loan collateral lines.
