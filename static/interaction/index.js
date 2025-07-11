// For student registration
function customAlert(message, formToReset = null) {
  const alertBox = document.getElementById('custom-alert');
  const alertMsg = document.getElementById('alert-message');
  const alertBar = document.getElementById('alert-bar');

  alertMsg.textContent = message;
  alertBox.classList.add('show');
  alertBox.classList.remove('hidden');

  // Restart animation
  alertBar.style.animation = 'none';
  alertBar.offsetHeight; // Force reflow
  alertBar.style.animation = null;

  // Hide and reset after 10 seconds
  setTimeout(() => {
    alertBox.classList.remove('show');
    alertBox.classList.add('hidden');
    if (formToReset) formToReset.reset();
  }, 10000); // You used 10 seconds here, and it's fine
}
const firstname = document.getElementById("s_firstname");
const lastname = document.getElementById("s_lastname");
const username = document.getElementById("s_username");
const email = document.getElementById("s_email");
const dob = document.getElementById("s_dob");
const gender = document.getElementById("s_gender");
const currentClass = document.getElementById("s_class");
const password1 = document.getElementById("s_password1");
const password2 = document.getElementById("s_password2");
const form = document.getElementById("student_register");
const errorDisplay = document.querySelector(".error");
//style for success registration
function customAlert(message, formToReset = null) {
  const alertBox = document.getElementById('custom-alert');
  const alertMsg = document.getElementById('alert-message');
  const alertBar = document.getElementById('alert-bar');

  alertMsg.textContent = message;
  alertBox.classList.add('show');
  alertBox.classList.remove('hidden');

  // Restart animation
  alertBar.style.animation = 'none';
  alertBar.offsetHeight; // Force reflow
  alertBar.style.animation = null;

  // Hide and reset after 5 seconds
  setTimeout(() => {
    alertBox.classList.remove('show');
    alertBox.classList.add('hidden');
    if (formToReset) formToReset.reset();
  }, 5000);
}
form.addEventListener("submit", function (e) {
  e.preventDefault(); // Prevent form reload

  const nameRegex = /^[A-Za-z]+$/;
  const passwordRegex = /^(?=.*[A-Za-z])(?=.*\d)(?=.*[!@#$%^&*]).{6,}$/;
  let notValid = false;

  // Firstname check
  if (firstname.value.trim() === "") {
    errorDisplay.textContent = "Firstname is required!";
    firstname.style.borderBottom = '4px solid red';
    firstname.focus();
    notValid = true;
  } else if (!nameRegex.test(firstname.value.trim())) {
    errorDisplay.textContent = "Firstname is invalid... Only letters are allowed";
    firstname.style.borderBottom = '4px solid red';
    firstname.focus();
    notValid = true;
  } else {
    firstname.style.borderBottom = "4px solid #31aa0b60";
  }

  // Lastname check
  if (lastname.value.trim() === "") {
    errorDisplay.textContent = "Lastname is required!";
    lastname.style.borderBottom = '4px solid red';
    lastname.focus();
    notValid = true;
  } else if (!nameRegex.test(lastname.value.trim())) {
    errorDisplay.textContent = "Lastname is invalid... Only letters are allowed";
    lastname.style.borderBottom = '4px solid red';
    lastname.focus();
    notValid = true;
  } else {
    lastname.style.borderBottom = "4px solid #31aa0b60";
  }

  // Username check
  if (username.value.trim() === "") {
    errorDisplay.textContent = "Your username field is empty";
    username.style.borderBottom = '4px solid red';
    username.focus();
    notValid = true;
  } else if (/^[A-Za-z]+$/.test(username.value.trim())) {
    errorDisplay.textContent = "Add a special character or number";
    username.style.borderBottom = '4px solid red';
    username.focus();
    notValid = true;
  } else if (
    /^[^\s]+$/.test(username.value.trim()) &&
    !/^[A-Za-z]+$/.test(username.value.trim())
  ) {
    username.style.borderBottom = "4px solid #31aa0b60";
  }

  // Email check
  if (email.value.trim() === "") {
    errorDisplay.textContent = "Email is required!";
    email.style.borderBottom = '4px solid red';
    email.focus();
    notValid = true;
  } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value.trim())) {
    errorDisplay.textContent = "Invalid email format!";
    email.style.borderBottom = '4px solid red';
    email.focus();
    notValid = true;
  } else {
    email.style.borderBottom = "4px solid #31aa0b60";
  }

  // DOB check
  if (dob.value.trim() === "") {
    errorDisplay.textContent = "Date of birth is required!";
    dob.style.borderBottom = '4px solid red';
    dob.focus();
    notValid = true;
  } else {
    dob.style.borderBottom = "4px solid #31aa0b60";
  }

  // Gender check
  if (gender.value.trim() === "") {
    errorDisplay.textContent = "Please select your gender!";
    gender.style.borderBottom = '4px solid red';
    gender.focus();
    notValid = true;
  } else {
    gender.style.borderBottom = "4px solid #31aa0b60";
  }

  // Current Class check
  if (currentClass.value.trim() === "") {
    errorDisplay.textContent = "Please select your current class!";
    currentClass.style.borderBottom = '4px solid red';
    currentClass.focus();
    notValid = true;
  } else {
    currentClass.style.borderBottom = "4px solid #31aa0b60";
  }

  // Password1 check
  if (password1.value.trim() === "") {
    errorDisplay.textContent = "Password is required!";
    password1.style.borderBottom = '4px solid red';
    password1.focus();
    notValid = true;
  } else if (!passwordRegex.test(password1.value.trim())) {
    errorDisplay.textContent = "Password must contain at least 1 letter, 1 number, 1 special character (!@#$...) and be 6 characters or more!";
    password1.style.borderBottom = '4px solid red';
    password1.focus();
    notValid = true;
  } else {
    password1.style.borderBottom = "4px solid #31aa0b60";
  }

  // Password2 check
  if (password2.value.trim() === "") {
    errorDisplay.textContent = "Please confirm your password!";
    password2.style.borderBottom = '4px solid red';
    password2.focus();
    notValid = true;
  } else if (password2.value.trim() !== password1.value.trim()) {
    errorDisplay.textContent = "Passwords do not match!";
    password2.style.borderBottom = '4px solid red';
    password2.focus();
    notValid = true;
  } else {
    password2.style.borderBottom = "4px solid #31aa0b60";
  }

  // Final form check
  if (!notValid) {
  const usernameText = username.value.trim();
  customAlert(`verify your email ${usernameText}`, form);
  form.submit()
}
});