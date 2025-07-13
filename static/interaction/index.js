document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("login_form");
  const id = document.getElementById("user_id");
  const pass = document.getElementById("l_password");
  const code = document.getElementById("invitation_code");

  form.addEventListener("submit", function(a) {
    a.preventDefault();

    if (id.value.trim() === "" && pass.value.trim() === "" && code.value.trim() === "") {
      id.style.borderBottom = '4px solid red';
      pass.style.borderBottom = '4px solid red';
      code.style.borderBottom = '4px solid red';
    } else if (id.value.trim() !== "" && pass.value.trim() === "") {
      id.style.borderBottom = '4px solid green';
      pass.style.borderBottom = '4px solid red';
    } else if (id.value.trim() === "" && pass.value.trim() !== "") {
      id.style.borderBottom = '4px solid red';
      pass.style.borderBottom = '4px solid green';
    } else if (id.value.trim() !== "" && pass.value.trim() !== "") {
      id.style.borderBottom = '4px solid green';
      pass.style.borderBottom = '4px solid green';
      code.style.borderBottom = '4px solid green';
      form.submit(); // ✅ only here it submits for ID+Password login
    } else if (id.value.trim() === "" && pass.value.trim() === "" && code.value.trim() !== "") {
      code.style.borderBottom = '4px solid green';
      form.submit(); // ✅ only here it submits for guest login
    }
  });
});