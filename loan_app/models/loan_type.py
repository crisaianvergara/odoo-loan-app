from odoo import api, fields, models


class LoanType(models.Model):
    _name = "loan.type"
    _description = "Loan Type"


    name = fields.Char("Type")
    description = fields.Char("Description")