from odoo import api, fields, models

PROCESSING_FEE = 3


class LoanBorrows(models.Model):
    _name = "loan.borrow"
    _description = "Loan Borrow"
    _rec_name = "borrower_id"

    # Fields
    borrower_id = fields.Many2one("loan.borrower", string="Borrower", required=True)
    loan_plan_id = fields.Many2one("loan.plan", string="Plan (months)", required=True)
    loan_type_id = fields.Many2one("loan.type", string="Type", required=True)
    loan_amount = fields.Float("Amount", required=True)
    active = fields.Boolean("Active?", default=True)

    # Summary
    loan_amount_summary = fields.Float("Loan Amount", compute="_compute_loan_amount_summary")
    processing_fee = fields.Float("Processing Fee", compute="_compute_processing_fee")
    amount_to_receive = fields.Float("Amount to Receive", compute="_compute_amount_to_receive")
    interest_rate = fields.Float("Interest Rate (%)", related="loan_plan_id.interest")
    term = fields.Char("Term", compute="_compute_term")
    monthly_amount_due = fields.Float("Monthly Amount Due", compute="_compute_monthly_amount_due")


    # Computed Fields
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
    def _compute_monthly_amount_due(self):
        """Compute monthly amount due."""
        for rec in self:
            if rec.loan_amount > 0 and rec.loan_plan_id:
                interest_value = rec.loan_amount * (rec.loan_plan_id.interest  / 100)
                total_interest_in_all_months = interest_value * int(rec.loan_plan_id.name)
                total_amount_to_pay = total_interest_in_all_months + rec.loan_amount
                rec.monthly_amount_due = total_amount_to_pay / int(rec.loan_plan_id.name)
            else: 
                rec.monthly_amount_due = 0

