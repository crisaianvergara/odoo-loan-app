{
    "name": "Loan Management",
    "summary": "Mange loan.",
    "description": "Manage loan.",
    "author": "Cris-aian Vergara",
    "website": "https://www.crisaianvergara.com",
    "category": "Finance/Loan",
    "version": "16.0.1.0.0",
    "depends": ["base", "loan_borrower", "mail"],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/loan_menus.xml",
        "views/loan_type_views.xml",
        "views/loan_plan_views.xml",
        "views/loan_borrow_views.xml",
        "views/loan_payment_views.xml",
        "report/loan_borrow_reports.xml",
    ],
    "demo": [],
    "sequence": -100,
    "application": True,
    "license": "LGPL-3"
}