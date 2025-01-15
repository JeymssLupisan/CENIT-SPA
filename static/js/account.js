const deleteBtns = document.querySelectorAll('.delete-btn');
const popup = document.getElementById('deletePopup');
const cancelBtn = document.querySelector('.cancel-btn');
const deleteForm = document.getElementById('deleteForm');
const appointmentDetails = document.getElementById('appointmentDetails');

deleteBtns.forEach(btn => {
    btn.addEventListener('click', (e) => {
        e.preventDefault();

        const appointmentId = btn.getAttribute('data-appointment-id');
        const serviceName = btn.getAttribute('data-service');
        const therapistName = btn.getAttribute('data-therapist');
        const appointmentDate = btn.getAttribute('data-date');
        const totalCost = btn.getAttribute('data-total-cost');
        const deleteUrl = btn.getAttribute('data-url').replace("0", appointmentId);

        deleteForm.action = deleteUrl;

        appointmentDetails.innerHTML = `
            <p><strong>Service:</strong> ${serviceName}</p>
            <p><strong>Therapist:</strong> ${therapistName}</p>
            <p><strong>Date:</strong> ${appointmentDate}</p>
            <p><strong>Total Cost:</strong> ₱${totalCost}</p>
        `;

        popup.classList.add('active');
    });
});

cancelBtn.addEventListener('click', () => {
    popup.classList.remove('active');
});
