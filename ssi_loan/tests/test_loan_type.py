# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged

STANDARD_LOAN_AMOUNT = 2400.0
STANDARD_INTEREST = 3.0
STANDARD_PERIOD = 6
STANDARD_FIRST_PAYMENT_DATE = "2024-02-01"
STANDARD_SCHEDULE_DATES = [
    "2024-02-01",
    "2024-03-01",
    "2024-04-01",
    "2024-05-01",
    "2024-06-01",
    "2024-07-01",
]


@tagged("post_install", "-at_install")
class TestLoanType(YamlTransactionCase):
    """Cover ``loan.type`` master data CRUD via YAML scenario.

    Also covers the pure-Python interest schedule tests for
    ``_compute_flat``, ``_compute_effective``, ``_compute_anuity``
    and their dispatcher ``_compute_interest`` (all ``@api.model``,
    so no ``loan.type`` record is needed as fixture).
    """

    def test_loan_type(self):
        """Run the ``test_data_loan_type.yaml`` scenario."""
        self.run_yaml_scenario("test_data_loan_type.yaml")

    def test_compute_flat(self):
        """Lock the flat-rate schedule for the standard test inputs.

        Pure Python — trigger P1 (L-01: the schedule is the
        method's return value; YAML ``action: call`` would discard
        it) and P2 (L-04: ``interest_amount`` is a division result
        compared with ``assertAlmostEqual``, since YAML ``equals``
        is a raw ``!=``). Locks row count, dates, and a constant
        per-row principal/interest for the standard inputs
        (``loan_amount=2400.0``, ``interest=3.0``, ``period=6``,
        ``first_payment_date="2024-02-01"``).
        """
        result = self.env["loan.type"]._compute_flat(
            STANDARD_LOAN_AMOUNT,
            STANDARD_INTEREST,
            STANDARD_PERIOD,
            STANDARD_FIRST_PAYMENT_DATE,
        )
        self.assertEqual(len(result), STANDARD_PERIOD)
        self.assertEqual(
            [row["schedule_date"] for row in result],
            STANDARD_SCHEDULE_DATES,
        )
        for row in result:
            self.assertAlmostEqual(row["principle_amount"], 400.0, places=2)
            self.assertAlmostEqual(row["interest_amount"], 6.0, places=2)

    def test_compute_effective(self):
        """Lock the effective-rate schedule for the standard inputs.

        Pure Python — trigger P1 (L-01: asserting the method's list
        return value, which YAML ``action: call`` would discard)
        and P2 (L-04: each declining-balance ``interest_amount`` is
        a division result compared with ``assertAlmostEqual``,
        since YAML ``equals`` is a raw ``!=``). Locks row count,
        dates, a constant principal, and the monotonically
        declining per-period interest for the standard inputs
        (``loan_amount=2400.0``, ``interest=3.0``, ``period=6``,
        ``first_payment_date="2024-02-01"``).
        """
        result = self.env["loan.type"]._compute_effective(
            STANDARD_LOAN_AMOUNT,
            STANDARD_INTEREST,
            STANDARD_PERIOD,
            STANDARD_FIRST_PAYMENT_DATE,
        )
        expected_interest = [6.0, 5.0, 4.0, 3.0, 2.0, 1.0]
        self.assertEqual(len(result), STANDARD_PERIOD)
        self.assertEqual(
            [row["schedule_date"] for row in result],
            STANDARD_SCHEDULE_DATES,
        )
        for row, interest in zip(result, expected_interest):
            self.assertAlmostEqual(row["principle_amount"], 400.0, places=2)
            self.assertAlmostEqual(row["interest_amount"], interest, places=2)
        interest_amounts = [row["interest_amount"] for row in result]
        self.assertLess(interest_amounts[-1], interest_amounts[0])

    def test_compute_anuity(self):
        """Lock the annuity schedule invariants for standard inputs.

        Pure Python — trigger P1 (L-01: asserting the method's list
        return value, which YAML ``action: call`` would discard)
        and P2 (L-04: the total installment and each per-period
        principal/interest are division results compared with
        ``assertAlmostEqual``, since YAML ``equals`` is a raw
        ``!=``). Locks row count, dates, a constant total
        installment (``principle_amount + interest_amount``) per
        period, and monotonic principal increase / interest
        decrease for the standard inputs (``loan_amount=2400.0``,
        ``interest=3.0``, ``period=6``,
        ``first_payment_date="2024-02-01"``).
        """
        result = self.env["loan.type"]._compute_anuity(
            STANDARD_LOAN_AMOUNT,
            STANDARD_INTEREST,
            STANDARD_PERIOD,
            STANDARD_FIRST_PAYMENT_DATE,
        )
        self.assertEqual(len(result), STANDARD_PERIOD)
        self.assertEqual(
            [row["schedule_date"] for row in result],
            STANDARD_SCHEDULE_DATES,
        )
        installments = [
            row["principle_amount"] + row["interest_amount"] for row in result
        ]
        for installment in installments[1:]:
            self.assertAlmostEqual(installment, installments[0], places=2)
        principles = [row["principle_amount"] for row in result]
        interests = [row["interest_amount"] for row in result]
        for index in range(1, len(result)):
            self.assertGreater(principles[index], principles[index - 1])
            self.assertLess(interests[index], interests[index - 1])

    def test_compute_interest_dispatch(self):
        """Dispatch each valid method to its matching direct call.

        Pure Python — trigger P1 (L-01: comparing the dispatcher's
        list return value against the specific method's return
        value, both of which YAML ``action: call`` would discard)
        and P2 (L-04: the compared rows carry division-derived
        ``interest_amount``/``principle_amount`` floats, the same
        kind of value this suite elsewhere compares with
        ``assertAlmostEqual`` instead of YAML's raw ``!=``).
        Calling ``_compute_interest`` with ``flat``/``effective``/
        ``anuity`` must return a list identical to calling the
        matching method directly, for the standard inputs.
        """
        loan_type = self.env["loan.type"]
        cases = (
            ("flat", loan_type._compute_flat),
            ("effective", loan_type._compute_effective),
            ("anuity", loan_type._compute_anuity),
        )
        for interest_method, direct_method in cases:
            dispatched = loan_type._compute_interest(
                STANDARD_LOAN_AMOUNT,
                STANDARD_INTEREST,
                STANDARD_PERIOD,
                STANDARD_FIRST_PAYMENT_DATE,
                interest_method,
            )
            direct = direct_method(
                STANDARD_LOAN_AMOUNT,
                STANDARD_INTEREST,
                STANDARD_PERIOD,
                STANDARD_FIRST_PAYMENT_DATE,
            )
            self.assertEqual(dispatched, direct)

    def test_compute_interest_unknown_method_returns_none(self):
        """Return ``None`` for an unrecognized ``interest_method``.

        Pure Python — trigger P1 (L-01: asserting the dispatcher's
        ``None`` return value, which YAML ``action: call`` would
        discard entirely) and P2 (L-04: cited for consistency with
        the sibling methods in this class that assert
        division-derived floats via ``assertAlmostEqual``; this
        particular case compares no floats). Calling
        ``_compute_interest`` with an unrecognized
        ``interest_method`` must return ``None``.
        """
        result = self.env["loan.type"]._compute_interest(
            STANDARD_LOAN_AMOUNT,
            STANDARD_INTEREST,
            STANDARD_PERIOD,
            STANDARD_FIRST_PAYMENT_DATE,
            "bogus",
        )
        self.assertIsNone(result)

    def test_compute_flat_end_of_month_edge_case(self):
        """Roll a 31st-of-month schedule onto a leap-year February.

        Pure Python — trigger P1 (L-01: asserting the method's list
        return value, which YAML ``action: call`` would discard)
        and P2 (L-04: cited for consistency with the sibling
        methods in this class that assert division-derived floats
        via ``assertAlmostEqual``; the assertions below compare
        only ``schedule_date`` strings). With
        ``first_payment_date="2024-01-31"`` and ``period=3``, the
        second installment must land on 2024-02-29 (leap year),
        neither failing nor shifting into March.
        """
        result = self.env["loan.type"]._compute_flat(
            STANDARD_LOAN_AMOUNT, STANDARD_INTEREST, 3, "2024-01-31"
        )
        expected_dates = ["2024-01-31", "2024-02-29", "2024-03-31"]
        self.assertEqual(len(result), 3)
        self.assertEqual([row["schedule_date"] for row in result], expected_dates)
