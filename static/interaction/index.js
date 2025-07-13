document.addEventListener("DOMContentLoaded", () => {
  const formIds = ["student_register", "admin_register", "teacher_register"];
  formIds.forEach(id => {
    const form = document.getElementById(id);
    if (form) attachValidation(form);
  });
});

function attachValidation(form) {
  const errorDisplay = form.querySelector(".error");
  const inputs = form.querySelectorAll("input, select");
  const password1 = form.querySelector("input[name='password'], input[name='initialPassword']");
  const password2 = form.querySelector("input[name='confirm_password'], input[name='finalPassword']");

  form.addEventListener("submit", function (e) {
    e.preventDefault();

    let notValid = false;
    errorDisplay.textContent = "";

    inputs.forEach(input => {
      const name = input.name;
      const value = input.value.trim();
      const type = input.type;

      input.style.borderBottom = ""; // Reset

      if (type === "text" && name.toLowerCase().includes("name")) {
        if (!/^[A-Za-z\s]+$/.test(value)) {
          showError(input, "Name must contain only letters and spaces");
        } else {
          markValid(input);
        }
      } else if (name === "username") {
        if (!/^(?=.*[A-Za-z])(?=.*[^A-Za-z\s]).{3,}$/.test(value)) {
          showError(input, "Username must include letters and at least one number or symbol");
        } else {
          markValid(input);
        }
      } else if (name === "invitation_code") {
        if (value === "") {
          showError(input, "Enter your invitation code");
        } else {
          markValid(input);
        }
      } else if (type === "email") {
        if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) {
          showError(input, "Invalid email format");
        } else {
          markValid(input);
        }
      } else if (type === "date") {
        if (!value) {
          showError(input, "Date is required");
        } else {
          markValid(input);
        }
      } else if (type === "tel") {
        if (!/^\d{11}$/.test(value)) {
          showError(input, "Enter a valid 11-digit phone number");
        } else {
          markValid(input);
        }
      } else if (type === "select-one" || type === "select-multiple") {
        if (!value) {
          showError(input, "Please select an option");
        } else {
          markValid(input);
        }
      }
    });

    // Password Validation
    if (password1 && password2) {
      const val1 = password1.value.trim();
      const val2 = password2.value.trim();
      const passwordRegex = /^(?=.*[A-Za-z])(?=.*\d)(?=.*[!@#$%^&*]).{6,}$/;

      if (!val1) {
        showError(password1, "Password is required");
      } else if (!passwordRegex.test(val1)) {
        showError(password1, "Password must include letter, number, special character, and be 6+ chars");
      } else {
        markValid(password1);
      }

      if (!val2) {
        showError(password2, "Please confirm your password");
      } else if (val1 !== val2) {
        showError(password2, "Passwords do not match");
      } else {
        markValid(password2);
      }
    }

    if (!notValid) {
      const username = form.querySelector("input[name='username']");
      const message = `Verify your email ${username?.value || "user"}`;
      customAlert(message, form);
      setTimeout(() => form.submit(), 500); // Submit after alert
    }

    function showError(input, msg) {
      errorDisplay.textContent = msg;
      input.style.borderBottom = "4px solid red";
      input.focus();
      notValid = true;
    }

    function markValid(input) {
      input.style.borderBottom = "4px solid #31aa0b60"; // green
    }
  });
}

// Custom alert (already in your code, optimized)
function customAlert(message, formToReset = null) {
  const alertBox = document.getElementById('custom-alert');
  const alertMsg = document.getElementById('alert-message');
  const alertBar = document.getElementById('alert-bar');

  alertMsg.textContent = message;
  alertBox.classList.add('show');
  alertBox.classList.remove('hidden');

  alertBar.style.animation = 'none';
  alertBar.offsetHeight;
  alertBar.style.animation = null;

  setTimeout(() => {
    alertBox.classList.remove('show');
    alertBox.classList.add('hidden');
    if (formToReset) formToReset.reset();
    const allInputs = formToReset?.querySelectorAll("input, select");
    allInputs?.forEach(el => el.style.borderBottom = "");
  }, 5000);
}

// login page
document.addEventListener("DOMContentLoaded",() => {
  const form = document.getElementById("login_form");
  const id = document.getElementById("user_id");
  const pass = document.getElementById("l_password");
  const code = document.getElementById("invitation_code");
  form.addEventListener("submit",function(a){
    a.preventDefault();
    if (id.value.trim() === "" && pass.value.trim() === "" && code.value.trim() === "") {
    id.style.borderBottom = '4px solid red';
    pass.style.borderBottom = '4px solid red';
    code.style.borderBottom = '4px solid red';
  }else if (id.value.trim() !== "" && pass.value.trim() === ""){
    id.style.borderBottom = '4px solid green';
    pass.style.borderBottom = '4px solid red';
  }else if (id.value.trim() === "" && pass.value.trim() !== ""){
    id.style.borderBottom = '4px solid red';
    pass.style.borderBottom = '4px solid green';
  }else if(id.value.trim() !== "" && pass.value.trim() !== ""){
    id.style.borderBottom = '4px solid green';
    pass.style.borderBottom = '4px solid green';
    code.style.borderBottom = '4px solid green';
  }else{
    id.style.borderBottom = '4px solid green';
    pass.style.borderBottom = '4px solid green';
    code.style.borderBottom = '4px solid green';
  }
  });
});