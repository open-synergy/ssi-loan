# Create Loan Additional Item

> **Module:** ssi_loan
>
> **Model:** `loan.additional_item`
>
> **Menu:** Loan > Configuration > Additional Items
>
> **Actor:** user in group _Loan Additional Item_ (`loan_additional_item_group`)

## Pre-Condition

- **Access:** User must belong to the **Loan Additional Item** access group
  (`loan_additional_item_group`).

## Flow

1. Open the **Loan > Configuration > Additional Items** menu.
2. Click the **Create** button.
3. Fill in the required fields:
   - **Loan Additional Item**: the name of the additional item (e.g. Admin Fee,
     Insurance).
   - **Code**: fill with **/** to let the system auto-assign a code, or enter a unique
     code manually.
4. Select the direction(s) this additional item applies to:
   - **Available for Loan Out**: check if this item can be used on **Loan Out**
     transactions.
   - **Available for Loan In**: check if this item can be used on **Loan In**
     transactions.
5. Open the **Loan Out Configuration** tab and fill in the accounts/journal used when
   this item is billed on a **Loan Out** transaction, if applicable:
   - **Receivable Journal**: journal used to post the receivable entry.
   - **Receivable Account**: account used to post the receivable.
   - **Contra-Receivable Account**: contra account used to post the receivable entry.
6. Open the **Loan In Configuration** tab and fill in the accounts/journal used when
   this item is billed on a **Loan In** transaction, if applicable:
   - **Payable Journal**: journal used to post the payable entry.
   - **Payable Account**: account used to post the payable.
   - **Contra-Payable Account**: contra account used to post the payable entry.
7. Click **Save**.

## Post-Condition

- A new record is created and is active by default.
- The record can now be selected as **Additional Items** on **Loan Type** records
  matching its direction, and instantiated on the related loan's payment schedule.
