from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models

from odoo.exceptions import ValidationError

# Constant Variables
PROCESSING_FEE = 3
LOAN_AMOUNT_MIN = 5000
LOAN_AMOUNT_MAX = 20000


# Functions
def get_amount_due(rec):
    interest_value = rec.loan_amount * (rec.loan_plan_id.interest  / 100)
    total_interest_in_all_months = interest_value * int(rec.loan_plan_id.name)
    total_amount_to_pay = total_interest_in_all_months + rec.loan_amount
    return total_amount_to_pay / int(rec.loan_plan_id.name)


class LoanBorrow(models.Model):
    _name = "loan.borrow"
    _description = "Loan Borrow"
    _rec_name = "borrower_id"

    # Fields
    borrower_id = fields.Many2one("loan.borrower", string="Borrower", required=True)
    loan_plan_id = fields.Many2one("loan.plan", string="Plan (months)", required=True)
    loan_type_id = fields.Many2one("loan.type", string="Type", required=True)
    loan_amount = fields.Float("Amount", required=True, default=LOAN_AMOUNT_MIN)
    active = fields.Boolean("Active?", default=True)

    # Summary
    loan_amount_summary = fields.Float("Loan Amount", compute="_compute_loan_amount_summary")
    processing_fee = fields.Float("Processing Fee", compute="_compute_processing_fee")
    amount_to_receive = fields.Float("Amount to Receive", compute="_compute_amount_to_receive")
    interest_rate = fields.Float("Interest Rate (%)", related="loan_plan_id.interest")
    term = fields.Char("Term", compute="_compute_term")
    amount_due = fields.Float("Amount Due", compute="_compute_amount_due")

    # State
    state = fields.Selection(
        string="Status",
        copy=False,
        default="draft",
        required=True,
        selection=[
            ("draft", "Draft"),
            ("submitted", "Submitted"),
            ("approved", "Approved"),
            ("canceled", "Canceled"),
        ],
    )

    related_loan_ids = fields.One2many(
        "loan.borrow", "borrower_id",
        string="Related Loans",
        compute="_compute_related_loans"
    ) # Review this field
    loan_payment_ids = fields.One2many("loan.payment", "loan_borrow_id", string="Loan Payments")


    # Computed Fields
    @api.depends("borrower_id")
    def _compute_related_loans(self): # Review this function
        """Compute related loans for the borrower."""
        for rec in self:
            related_loans = self.search(
                [
                    ("borrower_id", "=", rec.borrower_id.id),
                    ("id", "!=", rec.id),
                    ("state", "in", ["draft", "submitted", "approved"])
                ]
            )
            rec.related_loan_ids = related_loans


    @api.depends("loan_amount")
    def _compute_loan_amount_summary(self):
        """Compute loan amount."""
        for rec in self:
            rec.loan_amount_summary = rec.loan_amount


    @api.depends("loan_amount")
    def _compute_processing_fee(self):
        """Compute processing fee."""
        for rec in self:
            rec.processing_fee = rec.loan_amount * (PROCESSING_FEE / 100)

    
    @api.depends("loan_amount")
    def _compute_amount_to_receive(self):
        """Compute amount to receive."""
        for rec in self:
            rec.amount_to_receive = rec.loan_amount - rec.processing_fee
    

    @api.depends("loan_plan_id")
    def _compute_term(self):
        """Compute term."""
        for rec in self:
            if rec.loan_plan_id:
                rec.term = str(rec.loan_plan_id.name) + " months"
            else:
                rec.term = "0 month"
    

    @api.depends("loan_amount", "loan_plan_id")
    def _compute_amount_due(self):
        """Compute amount due."""
        for rec in self:
            if rec.loan_amount > 0 and rec.loan_plan_id:
                # Get amount due
                rec.amount_due = get_amount_due(rec)
            else: 
                rec.amount_due = 0


    # Python Constraints
    @api.constrains("loan_amount")
    def _validate_loan_amount(self):
        for rec in self:
            if not LOAN_AMOUNT_MIN <= rec.loan_amount <= LOAN_AMOUNT_MAX:
                raise ValidationError(f"Amount must be in between {LOAN_AMOUNT_MIN} to {LOAN_AMOUNT_MAX}.")
    

    @api.constrains("state")
    def _validate_related_loans(self): # Review this function
        """Validate related loan."""
        for rec in self:
            if rec.related_loan_ids and rec.state not in ["canceled"]:
                raise ValidationError("The borrower already has an active loan.")


    # Actions
    def action_submit(self):
        """Submit borrow."""
        if "canceled" in self.mapped("state"):
            raise ValidationError("Canceled borrows cannot be submit.")
        return self.write({"state": "submitted"})
    

    def action_approve(self):
        """Approved borrow."""
        for rec in self:
            rec.write({"state": "approved"})
            # Get amount due
            amount_due = get_amount_due(rec)
            payment_date = datetime.today().date()
            for _ in range(int(rec.loan_plan_id.name)):
                payment_date += relativedelta(months=1)
                rec.loan_payment_ids.create(
                    {
                        "loan_borrow_id": rec.id,
                        "payment_date": payment_date,
                        "amount_due": amount_due,
                    }
                )

    
    def action_cancel(self):
        """Cancel borrow."""
        if "approved" in self.mapped("state"):
            raise ValidationError("Approved borrows cannot be cancel.")
        return self.write({"state": "canceled"})