function confirmBack() {
return confirm("Are you sure you want to go back? Any unsaved changes will be lost.");
}

function validatePasswords() {
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirm_password').value;

    if (password !== confirmPassword) {
        alert("Passwords do not match. Please try again.");
        return false;
    }
    return true;
}

function validateFile() {
    var fileInput = document.getElementById('image');
    var filePath = fileInput.value;
    var allowedExtensions = /(\.jpg|\.jpeg|\.png)$/i;

    if (!allowedExtensions.exec(filePath)) {
        alert('Please upload an image file (jpg, jpeg, or png).');
        fileInput.value = '';
        return false;
    }

    return true;
}