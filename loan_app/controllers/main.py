from odoo import http
from odoo.http import request


class Loan(http.Controller):
    @http.route("/loan", type="http", auth="user", website=True)
    def loan_form(self, **kwargs):
        # Fetch loan plans and loan types from the database
        loan_plans = request.env['loan.plan'].sudo().search([])
        loan_types = request.env['loan.type'].sudo().search([])

        # Get the current user
        user = request.env.user

        return http.request.render("loan_app.create_loan", {
            'loan_plans': loan_plans,
            'loan_types': loan_types,
            'user': user,  # Pass the current user to the template
        })
    
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
        print("User:", user.name)

        return http.request.redirect("/")
    
