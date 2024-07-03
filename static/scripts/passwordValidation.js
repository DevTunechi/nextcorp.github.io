"use strict";

function validatePassword() {
    var password = document.getElementById("password");
    var confirm_password = document.getElementById("confirm_password");
    var message = document.getElementById("password_match");

    if (password.value != confirm_password.value) {
        message.innerHTML = "Passwords do not match";
        confirm_password.setCustomValidity("Passwords do not match");
    } else {
        message.innerHTML = "";
        confirm_password.setCustomValidity("");
    }
}
