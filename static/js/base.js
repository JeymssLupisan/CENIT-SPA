var loginBtn = document.getElementById("loginBtn");
var registerBtn = document.getElementById("registerBtn");
var loginForm = document.getElementById("login");
var registerForm = document.getElementById("register");
var navMenu = document.getElementById("navMenu");
var formBox = document.querySelector('.form-box');

function login() {
    loginForm.style.left = "0";
    registerForm.style.right = "100%";
    loginBtn.classList.add("white-btn");
    registerBtn.classList.remove("white-btn");
    loginForm.style.opacity = 1;
    registerForm.style.opacity = 0;
}

function register() {
    loginForm.style.left = "-100%";
    registerForm.style.right = "0";
    loginBtn.classList.remove("white-btn");
    registerBtn.classList.add("white-btn");
    loginForm.style.opacity = 0;
    registerForm.style.opacity = 1;
}

function myMenuFunction() {
    if (window.innerWidth <= 786) {
        if (navMenu.classList.contains("responsive")) {
            navMenu.classList.remove("responsive");
            formBox.style.display = "flex";
        } else {
            navMenu.classList.add("responsive");
            formBox.style.display = "none";
        }
    }
}

function togglePassword() {
    const passwordField = document.getElementById('password');
    const passwordCheck = document.getElementById('login-check');
    if (passwordCheck.checked) {
        passwordField.type = 'text';
    } else {
        passwordField.type = 'password';
    }
}
login();
