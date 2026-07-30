# Create Loan Out

> **Module:** ssi_loan_operating_unit
> **Extends:** ssi_loan — model `loan.out`, aksi `01-create`

## Additional Fields

When this module is installed, the create form gains one additional field, visible only
to users in the **Multiple Operating Unit** group
(`operating_unit.group_multi_operating_unit`):

- **Operating Unit**: the operating unit that owns this outgoing loan document. Not
  required. Automatically filled from the current user's default operating unit (falls
  back to an operating unit assigned to the user in the active company, if any). Change
  if needed.

## Modified — Record Visibility

- The **Loans Out** list is filtered by operating unit (record rule). A user only sees
  outgoing loan documents whose Operating Unit is one of the operating units assigned to
  them. This is not a Flow step.
