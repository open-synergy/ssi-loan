# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestLoanDocumensoSigning(YamlTransactionCase):
    """Cover the Documenso signing fields on ``loan.out``/``loan.in``.

    Verifies both models expose ``signature_request_ids`` and
    ``approval_signature_request_id`` empty right after creation,
    before any Documenso approval request is created.
    """

    def test_loan_documenso_signing(self):
        """Run the loan.out/loan.in Documenso signing scenario."""
        self.run_yaml_scenario("test_data_loan_documenso_signing.yaml")
