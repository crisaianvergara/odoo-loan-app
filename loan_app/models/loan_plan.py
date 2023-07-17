from odoo import api, fields, models


class LoanPlan(models.Model):
    _name = "loan.plan"
    _description = "Loan Plan"


    # Fields
    name = fields.Char("Plan", required = True)
    interest = fields.Float("Interest (%)", required = True)