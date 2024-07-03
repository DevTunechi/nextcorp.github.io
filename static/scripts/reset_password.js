"use strict";

document.addEventListener('DOMContentLoaded', function() {
    const resetPasswordButton = document.getElementById('reset-password-link');
    const corpIdInput = document.getElementById('corp_id');

    resetPasswordButton.addEventListener('click', function() {
        const corpId = corpIdInput.value;
        if (corpId) {
            window.location.href = `/corp_auth/reset?corp_id=${corpId}`;
        } else {
            alert('Please enter your Corp ID.');
        }
    });
});
