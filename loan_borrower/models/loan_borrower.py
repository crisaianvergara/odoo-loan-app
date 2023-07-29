import re
from datetime import date, timedelta
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class LoanBorrower(models.Model):
    _name = "loan.borrower"
    _description = "Loan Borrower"
    
    # Inheritance
    _inherit = ["mail.thread", "mail.activity.mixin"]

    # Delegation Inheritance
    _inherits = { "res.partner": "partner_id"}

    # SQL Constraints
    _sql_constraints = [
        (
            "check_address",
            "CHECK(length(address) > 5)", 
            "Address must be greater than 5 characters."
        ),
    ]
    
    # Fields
    partner_id = fields.Many2one("res.partner", delegate=True, ondelete="cascade", required=True)

    email = fields.Char(related="partner_id.email", readonly=False)
    mobile = fields.Char(related="partner_id.mobile", required=True, readonly=False)
    function = fields.Char(related="partner_id.function", required=True, readonly=False)

    address = fields.Char(string="Address", required=True)
    birth_date = fields.Date(string="Birth Date", required=True)
    age = fields.Integer(string="Age", readonly=True, compute="_compute_age", required=True)
    gender = fields.Selection(
        [
            ("male", "Male"),
            ("female", "Female"),
        ],
        string="Gender",
        required=True,
    )


    @api.depends('birth_date')
    def _compute_age(self):
        """Compute age."""
        for rec in self:
            if rec.birth_date:
                age = (date.today() - rec.birth_date) // timedelta(days=365.2425)
                if 18 <= age <= 60:
                    rec.age = age
                else:
                    raise ValidationError("Age must be between 18 to 60.")
            else:
                rec.age = 0
    

    # Python Constraints
    @api.constrains('mobile')
    def _validate_mobile(self):
        """Validate mobile: format(09279601094/+639279601094)."""
        if self.mobile:
            match = re.match(
                "((^(\+)(\d){12}$)|(^\d{11}$))",
                self.mobile
            )
            if match == None:
                raise ValidationError("Please enter a valid mobile number.")
            

    @api.constrains('email')
    def _validate_email(self):
        """Validate email address: format(crisaianvergara@gmail.com)."""
        # Error handling
        try:
            if self.email:
                match = re.match(
                    '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$',
                    self.email
                )
            if match == None:
                raise ValidationError('Please enter a valid email address!')
        except UnboundLocalError:
            print("UnboundLocalError triggered!")

    
    @api.constrains("function")
    def _validate_function(self):
        """Validate function/job position."""
        for rec in self:
            if len(rec.function) < 3:
                raise ValidationError("Job Position must be greater than 3 characters.")