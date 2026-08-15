# Activate Loan Additional Item

> **Module:** ssi_loan
>
> **Model:** `loan.additional_item`
>
> **Menu:** Loan > Configuration > Additional Items
>
> **Actor:** user in group _Loan Additional Item_ (`loan_additional_item_group`)
>
> **Active:** `false` → `true`
>
> **Requires:** `04-deactivate`

## Pre-Condition

- **Access:** User must belong to the **Loan Additional Item** access group
  (`loan_additional_item_group`).

## Flow

1. Open the **Loan > Configuration > Additional Items** menu.
2. Enable the **Archived** filter in the search bar.
3. Select one or more records to reactivate (check the checkbox).
4. Click **Action** > **Unarchive**.
5. Click **OK** to confirm.

## Post-Condition

- The records are restored and appear again in the default list view.
- The records can be selected again as **Additional Items** on new **Loan Type**
  records.
