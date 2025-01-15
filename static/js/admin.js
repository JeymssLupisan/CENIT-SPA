function showDashboard() {
    document.getElementById('dashboard').style.display = 'block';
    document.getElementById('admins').style.display = 'none';
    document.getElementById('users').style.display = 'none';
    document.getElementById('appointments').style.display = 'none';
    document.getElementById('services').style.display = 'none';
    document.getElementById('therapists').style.display = 'none';
    document.getElementById('availability').style.display = 'none';
}

function showAdmin() {
    document.getElementById('dashboard').style.display = 'none';
    document.getElementById('admins').style.display = 'block';
    document.getElementById('users').style.display = 'none';
    document.getElementById('appointments').style.display = 'none';
    document.getElementById('services').style.display = 'none';
    document.getElementById('therapists').style.display = 'none';
    document.getElementById('availability').style.display = 'none';
}

function showUser() {
    document.getElementById('dashboard').style.display = 'none';
    document.getElementById('admins').style.display = 'none';
    document.getElementById('users').style.display = 'block';
    document.getElementById('appointments').style.display = 'none';
    document.getElementById('services').style.display = 'none';
    document.getElementById('therapists').style.display = 'none';
    document.getElementById('availability').style.display = 'none';
}

function showAppointment() {
    document.getElementById('dashboard').style.display = 'none';
    document.getElementById('admins').style.display = 'none';
    document.getElementById('users').style.display = 'none';
    document.getElementById('appointments').style.display = 'block';
    document.getElementById('services').style.display = 'none';
    document.getElementById('therapists').style.display = 'none';
    document.getElementById('availability').style.display = 'none';
}

function showService() {
    document.getElementById('dashboard').style.display = 'none';
    document.getElementById('admins').style.display = 'none';
    document.getElementById('users').style.display = 'none';
    document.getElementById('appointments').style.display = 'none';
    document.getElementById('services').style.display = 'block';
    document.getElementById('therapists').style.display = 'none';
    document.getElementById('availability').style.display = 'none';
}

function showTherapist() {
    document.getElementById('dashboard').style.display = 'none';
    document.getElementById('admins').style.display = 'none';
    document.getElementById('users').style.display = 'none';
    document.getElementById('appointments').style.display = 'none';
    document.getElementById('services').style.display = 'none';
    document.getElementById('therapists').style.display = 'block';
    document.getElementById('availability').style.display = 'none';
}

function showAvailability() {
    document.getElementById('dashboard').style.display = 'none';
    document.getElementById('admins').style.display = 'none';
    document.getElementById('users').style.display = 'none';
    document.getElementById('appointments').style.display = 'none';
    document.getElementById('services').style.display = 'none';
    document.getElementById('therapists').style.display = 'none';
    document.getElementById('availability').style.display = 'block';
}

function searchAdmins() {
    const input = document.getElementById('adminSearch').value.toLowerCase();
    const rows = document.querySelectorAll('#adminTableBody tr');
    rows.forEach(row => {
        const cells = row.getElementsByTagName('td');
        row.style.display = Array.from(cells).some(cell => cell.textContent.toLowerCase().includes(input)) ? '' : 'none';
    });
}

function searchUsers() {
    const input = document.getElementById('userSearch').value.toLowerCase();
    const rows = document.querySelectorAll('#userTableBody tr');
    rows.forEach(row => {
        const cells = row.getElementsByTagName('td');
        row.style.display = Array.from(cells).some(cell => cell.textContent.toLowerCase().includes(input)) ? '' : 'none';
    });
}

function searchAppointments() {
    const input = document.getElementById('appointmentSearch').value.toLowerCase();
    const rows = document.querySelectorAll('#appointmentTableBody tr');
    rows.forEach(row => {
        const cells = row.getElementsByTagName('td');
        row.style.display = Array.from(cells).some(cell => cell.textContent.toLowerCase().includes(input)) ? '' : 'none';
    });
}

function searchServices() {
    const input = document.getElementById('serviceSearch').value.toLowerCase();
    const rows = document.querySelectorAll('#serviceTableBody tr');
    rows.forEach(row => {
        const cells = row.getElementsByTagName('td');
        row.style.display = Array.from(cells).some(cell => cell.textContent.toLowerCase().includes(input)) ? '' : 'none';
    });
}

function searchTherapists() {
    const input = document.getElementById('therapistSearch').value.toLowerCase();
    const rows = document.querySelectorAll('#therapistTableBody tr');
    rows.forEach(row => {
        const cells = row.getElementsByTagName('td');
        row.style.display = Array.from(cells).some(cell => cell.textContent.toLowerCase().includes(input)) ? '' : 'none';
    });
}

function searchAvailability() {
    const input = document.getElementById('availabilitySearch').value.toLowerCase();
    const rows = document.querySelectorAll('#therapistTableBody tr');
    rows.forEach(row => {
        const cells = row.getElementsByTagName('td');
        row.style.display = Array.from(cells).some(cell => cell.textContent.toLowerCase().includes(input)) ? '' : 'none';
    });
}

function showSection(section) {
    document.querySelectorAll('.content-section').forEach(function(sec) {
        sec.style.display = 'none';
    });
    document.getElementById(section).style.display = 'block';
}

window.onload = function() {
    const urlParams = new URLSearchParams(window.location.search);
    const section = urlParams.get('section');
    if (section) {
        showSection(section);
    } else {
        showSection('dashboard');
    }
};

function confirmLogout() {
      return confirm("Are you sure you want to log out?");
}
