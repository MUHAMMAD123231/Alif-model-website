document.getElementById("verify_form").addEventListener("submit", function (e) {
  e.preventDefault(); // Prevent page reload

  const code = document.getElementById("verification_code").value; // Get code

  fetch("/verify-email", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ code: code })
  })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        const studentId = data.id; // Changed to match Flask key

        alert(`✅ Email Verified!\nYour ID is: ${studentId}\nPlease copy and save it.`);

        // ✅ Correct redirection path
        window.location.href = data.redirect; // Flask returns /login
      } else {
        document.querySelector(".error-msg").textContent = data.message || "Invalid code.";
      }
    })
    .catch(err => {
      console.error("Verification error:", err);
    });
});