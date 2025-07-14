document.addEventListener("DOMContentLoaded", function () {
  const dashboard =
    document.querySelector(".admin-dashboard") ||
    document.querySelector(".student-dashboard") ||
    document.querySelector(".teacher-dashboard");

  if (!dashboard) return;

  const links = dashboard.querySelectorAll("aside nav a");
  const sections = dashboard.querySelectorAll(".section");
  const sidebar = dashboard.querySelector("aside");
  const hamburger = dashboard.querySelector("#hamburger");

  links.forEach(link => {
    link.addEventListener("click", function (e) {
      e.preventDefault();

      const targetId = this.getAttribute("href"); // like "#overview"
      const targetSection = dashboard.querySelector(targetId); // ✅ search inside dashboard only

      // Hide all sections
      sections.forEach(section => {
        section.classList.remove("active");
      });

      // Show only the selected one
      if (targetSection) {
        targetSection.classList.add("active");
      }

      // Close sidebar on mobile
      if (window.innerWidth <= 768) {
        sidebar.classList.remove("active");
      }
    });
  });

  // Sidebar toggle on hamburger click
  if (hamburger) {
    hamburger.addEventListener("click", function () {
      sidebar.classList.toggle("active");
    });
  }

  // Optional: Show the first section by default
  const defaultSection = dashboard.querySelector(".section");
  if (defaultSection) {
    defaultSection.classList.add("active");
  }
});