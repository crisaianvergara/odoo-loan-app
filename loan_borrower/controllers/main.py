from odoo import http
from odoo.http import request


class Borrower(http.Controller):
    @http.route("/profile", type="http", auth="public", website=True)
    def profile_form(self, **kwargs):
        return http.request.render("loan_app.create_profile", {})