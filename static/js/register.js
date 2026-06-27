
function setRole(role) {
  const userForm = document.getElementById("userForm");
  const ownerForm = document.getElementById("ownerForm");

  const userTab = document.getElementById("tab-user");
  const ownerTab = document.getElementById("tab-owner");

  if (role === "user") {
    userForm.style.display = "flex";
    ownerForm.style.display = "none";

    userTab.style.background = "var(--card)";
    ownerTab.style.background = "transparent";
  } else {
    userForm.style.display = "none";
    ownerForm.style.display = "flex";

    ownerTab.style.background = "var(--card)";
    userTab.style.background = "transparent";
  }
}

