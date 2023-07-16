from odoo import api, fields, models


class LoanPlan(models.Model):
    _name = "loan.plan"
    _description = "Loan Plan"


    name = fields.Char("Plan")
    interest = fields.Float("Interest (%)")