document.addEventListener("DOMContentLoaded", () => {
  const formIds = ["student_register", "admin_register", "teacher_register"];
  formIds.forEach(id => {
    const form = document.getElementById(id);
    if (form) attachValidation(form);
  });
});

function attachValidation(form) {
  const errorDisplay = form.querySelector("#form-error") || form.querySelector(".error");
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

      // --- Name fields ---
      if (type === "text" && name.toLowerCase().includes("name") && name.toLowerCase() !== "username") {
        if (!value) {
          showError(input, "Name field cannot be empty");
        } else if (!/^[A-Za-z\s]+$/.test(value)) {
          showError(input, "Name must contain only letters and spaces");
        } else {
          markValid(input);
        }
      }

      // --- Username field (allow emojis, symbols, letters, numbers — no spaces) ---
      else if (name.toLowerCase() === "username") {
        const usernameRegex = /^[\p{L}\p{N}\p{P}\p{S}]+$/u; // no spaces
        if (!value) {
          showError(input, "Username is required");
        } else if (!usernameRegex.test(value)) {
          showError(input, "Username can contain letters, emojis, numbers & symbols — no spaces");
        } else {
          markValid(input);
        }
      }

      // --- Email field ---
      else if (type === "email") {
        if (!value) {
          showError(input, "Email is required");
        } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) {
          showError(input, "Enter a valid email address");
        } else {
          markValid(input);
        }
      }

      // --- Phone number ---
      else if (type === "tel") {
        if (!value) {
          showError(input, "Phone number is required");
        } else if (!/^\d{11}$/.test(value)) {
          showError(input, "Phone number must be exactly 11 digits");
        } else {
          markValid(input);
        }
      }

      // --- Date of birth ---
      else if (type === "date") {
        if (!value) {
          showError(input, "Date of birth is required");
        } else {
          markValid(input);
        }
      }

      // --- Invitation Code ---
      else if (name === "invitation_code") {
        if (!value) {
          showError(input, "Enter your invitation code");
        } else {
          markValid(input);
        }
      }

      // --- Gender, Class, Role selections ---
      else if (type === "select-one" || type === "select-multiple") {
        if (!value) {
          showError(input, "Please select an option");
        } else {
          markValid(input);
        }
      }
    });

    // --- Password validation ---
    if (password1 && password2) {
      const val1 = password1.value.trim();
      const val2 = password2.value.trim();
      const passReg = /^(?=.*[A-Za-z])(?=.*\d)(?=.*[!@#$%^&*]).{6,}$/;

      if (!val1) {
        showError(password1, "Password is required");
      } else if (!passReg.test(val1)) {
        showError(password1, "Password must include letter, number, special char & be 6+ chars");
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

    // --- Final submission if no errors ---
    if (!notValid) {
      const username = form.querySelector("input[name='username'], input[name='Username']");
      const message = `Verify your email ${username?.value || "user"}`;
      customAlert(message, form);
      setTimeout(() => form.submit(), 600);
    }

    // --- Error styling ---
    function showError(input, msg) {
      errorDisplay.textContent = msg;
      input.style.borderBottom = "4px solid red";
      input.focus();
      notValid = true;
    }

    function markValid(input) {
      input.style.borderBottom = "4px solid #31aa0b60";
    }
  });
}

// --- Custom alert function ---
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