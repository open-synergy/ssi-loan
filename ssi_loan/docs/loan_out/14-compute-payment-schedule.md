# Compute Payment Schedule — Loan Out

## Pre-Condition

- **Record:** Record is in **Draft** status.
- **Record:** **Loan Type**, **Loan Amount**, **Interest (p.a)**, **Loan Period**, and
  **First Payment Date** are already filled in.
- **Access:** User must belong to the **User** access group (`loan_out_user_group`).

## Flow

1. Open the **Loan > Loans Out** menu.
2. Open the record.
3. Open the **Repayment Term** tab.
4. Click the **Payment Schedule** button.

## Post-Condition

- Any existing **Payment Schedule** lines are deleted and rebuilt from the loan type's
  interest method (**Anuity**, **Flat**, or **Effective**), one line per installment.
- **Total Principle Amount** and **Total Interest Amount** are recalculated.
