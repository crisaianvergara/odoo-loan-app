from odoo import api, fields, models

from odoo.exceptions import ValidationError


class LoanType(models.Model):
    _name = "loan.type"
    _description = "Loan Type"

    # SQL Constraints
    _sql_constraints = [
        ("check_unique_name", "UNIQUE(name)", "The Type must be unique."),
    ]

    # Fields
    name = fields.Char("Type", required=True)


    # Python Constraints
    @api.constrains("name")
    def _validate_name(self):
        """Validate name."""
        for rec in self:
            if len(rec.name) < 3:
                raise ValidationError("Type must be greater than 3 characters.")