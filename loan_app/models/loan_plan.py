from odoo import api, fields, models

from odoo.exceptions import ValidationError


class LoanPlan(models.Model):
    _name = "loan.plan"
    _description = "Loan Plan"
    _order = 'name'

    # SQL Constraints
    _sql_constraints = [
            ("check_unique_name", "UNIQUE(name)", "The Plan (months) must be unique."),
            ("check_positive_interest", "CHECK(interest > 0)", "The Interest (%) must be positive."),
        ]


    # Fields
    name = fields.Char("Plan (months)", required=True)
    interest = fields.Float("Interest (%)", required=True)


    # Python Constraints
    @api.constrains("name")
    def _validate_name(self):
        """Validate name."""
        for rec in self:
            if not rec.name.isdigit():
                raise ValidationError("Plan (months) must be a positive number.")
            elif not 1 <= int(rec.name) <= 12:
                raise ValidationError("Plan (months) must be in between 1 to 12.")