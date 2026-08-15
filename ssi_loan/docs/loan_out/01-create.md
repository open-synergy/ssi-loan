# Create Loan Out

> **Module:** ssi_loan
> **Model:** `loan.out`
> **Menu:** Loan > Loans Out
> **Actor:** user in group *User* (`loan_out_user_group`)
> **State:** — → `draft`

## Pre-Condition

- **Access:** User must belong to the **User** access group (`loan_out_user_group`),
  which also grants the **Viewer** access needed to open the **Loans Out** menu.

## Flow

1. Open the **Loan > Loans Out** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the required fields:
   - **Date Transaction**: the date of the loan transaction.
   - **Date Cut-Off**: the interest cut-off date, if applicable.
   - **Partner**: select the borrower/lender partner.
   - **Request Date**: defaults to today's date. Change if needed.
   - **Loan Type**: select a loan type with **Direction** set to **Out**.
   - **Loan Amount**: fill in the principal amount to be disbursed.
   - **Currency**: select the currency used for this loan.
   - **Rate Inverted**: tick if the exchange rate direction must be inverted, if
     applicable.
   - **Rate**: automatically filled from **Date Transaction**. Change if needed.
   - **Interest (p.a)**: automatically filled from **Loan Type**. Change if needed.
   - **Loan Period**: fill in the number of installments.
   - **First Payment Date**: fill in the date of the first installment.
4. Optionally add lines in the **Collaterals** tab. Repeat the following steps as many
   times as needed:
   - Click **Add a line**.
   - Fill in each line with:
     - **Type**: the collateral type.
     - **Name**: a description of the collateral.
5. Click **Save**.

## Post-Condition

- A new record is created in **Draft** status.
