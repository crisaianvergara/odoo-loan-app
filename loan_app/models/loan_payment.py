from datetime import date

from odoo import api, fields, models


class LoanPayment(models.Model):
    _name = "loan.payment"
    _description = "Loan Payment"

    # Fields
    loan_borrow_id = fields.Many2one("loan.borrow", string="Borrower", required=True)
    payment_date = fields.Date("Payment Date", required=True)
    amount_due = fields.Float("Amount Due", required=True)
    paid_date = fields.Date("Paid Date")

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
    # Connected tp pay Button: Review this code
    show_pay_button = fields.Boolean(
        "Show Pay Button",
        compute="_compute_show_pay_button"
    )
    # New field to store the nearest unpaid payment date
    next_payment_date = fields.Date("Next Payment Date", compute="_compute_next_payment_date")

    # Computed Fields
    @api.depends("payment_date", "state")
    def _compute_show_pay_button(self):
        """Only show the pay button on the next payment date."""
        today = date.today()
        for rec in self:
            rec.show_pay_button = (
                rec.state == 'unpaid' and rec.payment_date == rec.next_payment_date
            )
    
    # Review this code
    @api.depends('loan_borrow_id.loan_payment_ids')
    def _compute_next_payment_date(self):
        """Computed field to calculate the next unpaid payment date."""
        today = date.today()
        for rec in self:
            unpaid_payments = rec.loan_borrow_id.loan_payment_ids.filtered(lambda r: r.state == 'unpaid' and r.payment_date >= today)
            if unpaid_payments:
                nearest_unpaid_payment = unpaid_payments.sorted(key=lambda r: r.payment_date)[0]
                rec.next_payment_date = nearest_unpaid_payment.payment_date
            else:
                rec.next_payment_date = False


    # Actions
    def action_pay(self):
        """Pay loan amount due."""
        paid_date = date.today()
        self.write({"state": "paid", "paid_date": paid_date})

        # Check if there are any payments with state 'unpaid' in the loan
        unpaid_payments = self.loan_borrow_id.loan_payment_ids.filtered(lambda r: r.state == 'unpaid')
        if not unpaid_payments:
            self.loan_borrow_id.write({'state': 'closed'})