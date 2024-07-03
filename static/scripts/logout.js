"use strict";

document.addEventListener('DOMContentLoaded', function() {
    var logoutBtn = document.getElementById('logoutBtn');

    logoutBtn.addEventListener('click', function() {
        var xhr = new XMLHttpRequest();
        xhr.open('GET', '/auth/logout', true);
        xhr.onreadystatechange = function() {
            if (xhr.readyState === XMLHttpRequest.DONE) {
                if (xhr.status === 200) {
                    var response = JSON.parse(xhr.responseText);
                    alert(response.message);
                    window.location.href = '/corp_auth/login';
                } else {
                    console.error('Logout failed:', xhr.status);
                    alert('Logout failed. Please try again.');
                }
            }
        };
        xhr.send();
    });
});
