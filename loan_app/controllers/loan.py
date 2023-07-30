from odoo import http
from odoo.http import request
from ..models.loan_borrow import (
    PROCESSING_FEE,
    LOAN_AMOUNT_MIN,
    LOAN_AMOUNT_MAX,
    send_email_submit
)


def check_active_loan():
    # Check if the user already has loans in draft, submitted, or approved states
    existing_loan = request.env["loan.borrow"].sudo().search([
        ("borrower_id", "=", request.env.user.partner_id.id),
        ("state", "in", ["draft", "submitted", "approved"]),
    ])
    return existing_loan


class Loan(http.Controller):
    @http.route("/loan", type="http", auth="user", website=True)
    def loan(self, **kwargs):
        # Get the current user
        current_user = request.env.user.partner_id.id

        # Retrieve only the data of the current user from the loan.borrow
        loans = request.env["loan.borrow"].sudo().search([("borrower_id", "=", current_user)])

        return request.render(
            "loan_app.loan",
            {
                "loans": loans,
                "existing_loan": check_active_loan(),
            }
        )


    @http.route("/loan/new", type="http", auth="user", website=True)
    def new_loan(self, **kwargs):
        # Validate active loan
        if check_active_loan():
            return request.redirect("/loan")

        # Fetch loan plans and loan types from the database
        loan_plans = request.env['loan.plan'].sudo().search([])
        loan_types = request.env['loan.type'].sudo().search([])

        # Get the current user
        current_user = request.env.user

        return request.render(
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
    
    @http.route("/loan/submit", type="http", auth="user", website=True, methods=["POST"])
    def submit_loan(self, **kwargs):
        # Retrieve the form data
        loan_amount = float(kwargs.get('loan_amount', 0))
        loan_plan_id = int(kwargs.get('loan_plan', 0))
        loan_type_id = int(kwargs.get('loan_type', 0))

        # Get the current user
        user = request.env.user

        # Create a new record in the loan.borrow model
        loan_borrow = request.env["loan.borrow"].sudo().create({
            "borrower_id": user.partner_id.id,
            "loan_plan_id": loan_plan_id,
            "loan_type_id": loan_type_id,
            "loan_amount": loan_amount,
            "state": "submitted",
        })
        send_email_submit(request, loan_borrow.id)
        return request.redirect("/")
    
