# Create Loan Type

> **Module:** ssi_loan
>
> **Model:** `loan.type`
>
> **Menu:** Loan > Configuration > Loan Types
>
> **Actor:** user in group _Loan Type_ (`loan_type_group`)

## Pre-Condition

- **Access:** User must belong to the **Loan Type** access group (`loan_type_group`).

## Flow

1. Open the **Loan > Configuration > Loan Types** menu.
2. Click the **Create** button.
3. Fill in the required fields:
   - **Loan Type**: the name/label of this loan type.
   - **Code**: fill with **/** to let the system auto-assign a code, or enter a unique
     code manually.
   - **Direction**: select **In** or **Out** to determine whether this loan type is used
     on **Loan In** or **Loan Out** transactions.
   - **Currency**: select the currency used for this loan type.
4. Open the **Loan Configuration** tab and fill in:
   - **Interest Method**: select the interest calculation method used to build the
     payment schedule — **Anuity**, **Flat**, or **Effective**.
   - **Maximum Loan Amount**: fill in the maximum loan amount allowed for this type.
   - **Interest Amount**: fill in the interest rate, if applicable.
   - **Maximum Installment Period**: fill in the maximum number of installments allowed,
     if applicable.
5. Open the **Accounting** tab and fill in the accounts/journals used when a loan of
   this type is realized:
   - **Realization Journal**: journal used to post the realization entry.
   - **Realization Account**: cross-account used as the debit account for **Loan In** or
     the credit account for **Loan Out**.
   - **Short-Term Principle Account**: account used for the short-term portion of the
     principal, if applicable.
   - **Long-Term Principle Account**: account used for the long-term portion of the
     principal, if applicable.
   - **Rounding Account**: account used to post rounding differences, if applicable.
   - **Interest Journal**: journal used to post interest entries, if applicable.
   - **Interest Account**: account used to post interest, if applicable.
   - **Interest Income Account**: account used to post interest income, if applicable.
6. Open the **Additional Item** tab and select the **Additional Items** allowed for this
   loan type, if any. Only additional items matching the selected **Direction** can be
   selected.
7. Click **Save**.

## Post-Condition

- A new record is created and is active by default.
- The record can now be selected as **Loan Type** on **Loan In**/**Loan Out**
  transactions.
