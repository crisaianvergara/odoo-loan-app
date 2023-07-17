from odoo import api, fields, models


class LoanBorrows(models.Model):
    _name = "loan.borrow"
    _description = "Loan Borrow"
    _rec_name = "borrower_id"

    # Fields
    borrower_id = fields.Many2one("loan.borrower", string="Borrower", required=True)
    loan_plan = fields.Many2one("loan.plan", string="Plan (months)", required=True)
    loan_type = fields.Many2one("loan.type", string="Type", required=True)
    loan_amount = fields.Float("Amount", required=True)
    active = fields.Boolean("Active?", default=True)

    # Summary
    loan_amount_summary = fields.Char("Loan Amount")
    processing_fee = fields.Float("Processing Fee")
    amount_to_receive = fields.Float("Amount to Receive")
    interest_rate = fields.Float("Interest Rate (%)")
    term = fields.Char("Term (months)")
    amount_due = fields.Float("Amount Due")


