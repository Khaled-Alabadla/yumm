function setRole(role) {
  const roleInput = document.getElementById("roleInput");

  const userForm = document.getElementById("userForm");
  const ownerForm = document.getElementById("ownerForm");

  const userTab = document.getElementById("tab-user");
  const ownerTab = document.getElementById("tab-owner");

  if (roleInput) {
    roleInput.value = role;
  }

  if (userForm && ownerForm) {
    userForm.style.display = role === "user" ? "flex" : "none";
    ownerForm.style.display = role === "user" ? "none" : "flex";
  }

  if (userTab && ownerTab) {
    if (role === "user") {
      userTab.style.cssText =
        "background: var(--card); color: var(--text-primary); box-shadow: 0 1px 4px rgba(0,0,0,.08);";
      ownerTab.style.cssText =
        "background: transparent; color: var(--text-secondary);";
    } else {
      ownerTab.style.cssText =
        "background: var(--card); color: var(--text-primary); box-shadow: 0 1px 4px rgba(0,0,0,.08);";
      userTab.style.cssText =
        "background: transparent; color: var(--text-secondary);";
    }
  }
}


function togglePass(inputId, iconId) {
  const input = document.getElementById(inputId);
  const icon = document.getElementById(iconId);

  if (!input || !icon) return;

  if (input.type === "password") {
    input.type = "text";
    icon.className = "fa-solid fa-eye-slash text-sm";
  } else {
    input.type = "password";
    icon.className = "fa-solid fa-eye text-sm";
  }
}