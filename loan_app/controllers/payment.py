from odoo import http
from odoo.http import request


class Payment(http.Controller):
    @http.route("/payment", type="http", auth="user", website=True)
    def payment(self, **kwargs):
        current_user = request.env.user
        loans = request.env["loan.borrow"].sudo().search([
            ("borrower_id", "=", current_user.partner_id.id),
            ("state", "in", ["approved"]),
        ])
        payments = request.env["loan.payment"].sudo().search([
            ("loan_borrow_id", "=", loans[0].id),
        ])

        return request.render(
            "loan_app.payment",
            {
                "current_user_name": current_user.name,
                "payments": payments
            }
        )