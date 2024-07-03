"use strict";

// const employeeId = "{{ session.get('employee_id') }}";

function fetchEmployeeCheckers(employeeId) {
    const apiUrl = `http://0.0.0.0:5000/api/employees/${employeeId}/checkers`;

    fetch(apiUrl, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('NetworkError');
        }
        return response.json();
    })
    .then(data => {
        const checkersContainer = document.getElementById('checkers');
        checkersContainer.innerHTML = '';

        if (data.length === 0) {
            checkersContainer.textContent = 'No check-in/check-out data available.';
            return;
        }

        // Find the most recent check-in and check-out times
        let lastCheckin = null;
        let lastCheckout = null;

        for (let entry of data) {
            if (!lastCheckin || new Date(entry.checkin) > new Date(lastCheckin)) {
                lastCheckin = entry.checkin;
            }
            if (entry.checkout && (!lastCheckout || new Date(entry.checkout) > new Date(lastCheckout))) {
                lastCheckout = entry.checkout;
            }
        }

        // Display the last check-in and check-out times
        displayCheckersData(lastCheckin, lastCheckout);
    })
    .catch(error => {
	const checkersContainer = document.getElementById('checkers');
        if (error.message === 'NetworkError') {
            checkersContainer.textContent = 'Failed to fetch data: Network Error';
        } else {
            const checkersContainer = document.getElementById('checkers');
            checkersContainer.textContent = `Failed to fetch data: ${error.message}`;
        }
    });
}

function displayCheckersData(lastCheckin, lastCheckout) {
    const checkersContainer = document.getElementById('checkers');
    checkersContainer.innerHTML = ''; // Clear any existing content

    const checkerDiv = document.createElement('div');
    checkerDiv.classList.add('checker-entry');

    const checkinTime = document.createElement('p');
    checkinTime.textContent = `Last Check-in: ${lastCheckin}`;

    const checkoutTime = document.createElement('p');
    checkoutTime.textContent = `Last Check-out: ${lastCheckout || 'N/A'}`;

    checkerDiv.appendChild(checkinTime);
    checkerDiv.appendChild(checkoutTime);

    checkersContainer.appendChild(checkerDiv);
}

// Fetch and display the check-in/check-out times when the page loads
document.addEventListener('DOMContentLoaded', () => {
    if (employeeId) {
        fetchEmployeeCheckers(employeeId);
    } else {
        const checkersContainer = document.getElementById('checkers');
        checkersContainer.textContent = 'Employee ID not available.';
    }
});
