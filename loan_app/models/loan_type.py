from odoo import api, fields, models


class LoanType(models.Model):
    _name = "loan.type"
    _description = "Loan Type"


    # Fields
    name = fields.Char("Type", required = True)
    description = fields.Char("Description")