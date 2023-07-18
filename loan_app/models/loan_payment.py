from odoo import api, fields, models


class LoanPayment(models.Model):
    _name = "loan.payment"
    _description = "Loan Payment"

    # Fields
    loan_borrow_id = fields.Many2one("loan.borrow", string="Borrower", required=True)
    payment_date = fields.Date("Payment Date", required=True)
    amount_due = fields.Float("Amount Due", required=True)

    # State
    state = fields.Selection(
        string="Status",
        copy=False,
        default="unpaid",
        required=True,
        selection=[
            ("unpaid", "Unpaid"),
            ("paid", "Paid"),
        ],
    )