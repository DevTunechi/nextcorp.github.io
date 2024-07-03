"use strict";


function deleteEmployee(employeeId) {
    fetch(`/admin/dashboard/delete/${employeeId}`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert("Error deleting employee: " + data.error);
        } else {
            alert(data.message);
            location.reload();
        }
    })
    .catch(error => {
        alert("Error deleting employee: " + error.message);
    });
}

function updateCorpPosition() {
    var isHrCheckbox = document.getElementById("is_hr");
    var corpPositionInput = document.getElementById("corp_position");
    if (isHrCheckbox.checked) {
        corpPositionInput.value = "Human Resources";
    }
}

document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('show-employees').addEventListener('click', function () {
        document.getElementById('employee-form').style.display = 'none';
        document.getElementById('employee-list').style.display = 'block';
    });

    document.getElementById('add-employee').addEventListener('click', function () {
        document.getElementById('employee-list').style.display = 'none';
        document.getElementById('employee-form').style.display = 'block';
    });
});
