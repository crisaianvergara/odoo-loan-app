from odoo import api, fields, models


class LoanBorrowInherit(models.Model):
    _inherit = "loan.borrow"


    def action_approve(self):
        res = super().action_approve()
        print("TRIGGERED INVOICE!")
        return res