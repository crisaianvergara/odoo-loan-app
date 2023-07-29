from odoo import http
from odoo.http import request
from ...loan_app.models.loan_borrow import PROCESSING_FEE, LOAN_AMOUNT_MIN, LOAN_AMOUNT_MAX


class LoanForm(http.Controller):
    @http.route("/loan", type="http", auth="user", website=True)
    def loan_form(self, **kwargs):
        # Fetch loan plans and loan types from the database
        loan_plans = request.env['loan.plan'].sudo().search([])
        loan_types = request.env['loan.type'].sudo().search([])

        # Get the current user
        current_user = request.env.user

        return http.request.render(
            "loan_app.loan_form", 
            {
                'loan_plans': loan_plans,
                'loan_types': loan_types,
                'current_user': current_user,
                'processing_fee': PROCESSING_FEE,
                'loan_amount_min': LOAN_AMOUNT_MIN,
                'loan_amount_max': LOAN_AMOUNT_MAX,
            }
        )
    
    @http.route("/submit_loan", type="http", auth="user", website=True, methods=["POST"])
    def submit_loan(self, **post):
        # Retrieve the form data
        loan_amount = float(post.get('loan_amount', 0))
        loan_plan_id = int(post.get('loan_plan', 0))
        loan_type_id = int(post.get('loan_type', 0))

        # Get the current user
        user = request.env.user

        # Print the form data to the console
        print("Loan Amount:", loan_amount)
        print("Loan Plan ID:", loan_plan_id)
        print("Loan Type ID:", loan_type_id)
        print("User:", user.id)

        # Create a new record in the loan.borrow model
        loan_borrow = request.env["loan.borrow"].sudo().create({
            "borrower_id": user.partner_id.id,
            "loan_plan_id": loan_plan_id,
            "loan_type_id": loan_type_id,
            "loan_amount": loan_amount,
            "state": "submitted",
        })

        return http.request.redirect("/")
    
