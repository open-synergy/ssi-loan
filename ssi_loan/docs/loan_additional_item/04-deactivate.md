# Deactivate Loan Additional Item

> **Module:** ssi_loan
> **Model:** `loan.additional_item`
> **Menu:** Loan > Configuration > Additional Items
> **Actor:** user in group *Loan Additional Item* (`loan_additional_item_group`)
> **Active:** `true` → `false`
> **Requires:** `01-create`

## Pre-Condition

- **Access:** User must belong to the **Loan Additional Item** access group
  (`loan_additional_item_group`).

## Flow

1. Open the **Loan > Configuration > Additional Items** menu.
2. Select one or more records to deactivate (check the checkbox).
3. Click **Action** > **Archive**.
4. Click **OK** to confirm.

## Post-Condition

- The records are archived and no longer appear in the default list view.
- Deactivated records cannot be selected as **Additional Items** on new **Loan Type**
  records.
- Transactions that already use this record can still be viewed.
