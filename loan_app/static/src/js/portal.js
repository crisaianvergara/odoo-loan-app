odoo.define('loan_app.portal', function (require) {
    'use strict';

    var core = require('web.core');
    var _t = core._t;

    $(document).ready(function () {
        // Add an event listener to the form submit button
        $('#loan-form').on('submit', function (event) {
            // Prevent the form from being submitted
            event.preventDefault();

            // Get the values of the input fields
            var name = $('#name').val();
            var loanAmount = $('#loan_amount').val();
            var loanPlan = $('#loan_plan').val();
            var loanType = $('#loan_type').val();

            // Check if any of the fields are empty
            if (!name || !loanAmount || !loanPlan || !loanType) {
                // Display an error message to the user
                alert(_t("All fields are required. Please fill in all the fields."));
            } else {
                // If all fields are filled, proceed with form submission
                this.submit();
            }
        });
    });
});
