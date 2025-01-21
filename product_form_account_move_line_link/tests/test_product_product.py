from odoo import Command
from odoo.tests import tagged

from odoo.addons.account.tests.common import AccountTestInvoicingCommon


@tagged("post_install", "-at_install")
class TestProductProduct(AccountTestInvoicingCommon):
    def setUp(self):
        super().setUp()
        self.product = self.env.ref("product.product_product_11")
        self.product_b = self.env.ref("product.product_product_11b")
        self.product_template = self.env.ref(
            "product.product_product_11_product_template"
        )
        self.account_move_line_model = self.env["account.move.line"]

    def test_compute_account_move_lines_count(self):
        bill = self.env["account.move"].create(
            [
                {
                    "move_type": "in_invoice",
                    "invoice_date": "2024-05-01",
                    "partner_id": self.partner_a.id,
                    "invoice_line_ids": [
                        Command.create(
                            {
                                "name": "line",
                                "price_unit": 1000,
                                "quantity": 1,
                                "product_id": self.product.id,
                            }
                        )
                    ],
                }
            ]
        )
        bill.action_post()

        self.product._compute_account_move_lines_count()
        self.product_b._compute_account_move_lines_count()
        self.product_template._compute_account_move_lines_count()
        self.assertEqual(self.product.account_move_lines_count, 1)
        self.assertEqual(self.product_b.account_move_lines_count, 0)
        self.assertEqual(self.product_template.account_move_lines_count, 1)
