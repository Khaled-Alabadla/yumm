function setRole(role) {
  const roleInput = document.getElementById('roleInput');
  const userTab  = document.getElementById('tab-user');
  const ownerTab = document.getElementById('tab-owner');
  
  if (roleInput) roleInput.value = role;
  
  if (userTab && ownerTab) {
    if (role === 'user') {
      userTab.style.cssText  = 'background: var(--card); color: var(--text-primary); box-shadow: 0 1px 4px rgba(0,0,0,0.08);';
      ownerTab.style.cssText = 'background: transparent; color: var(--text-secondary);';
    } else {
      ownerTab.style.cssText = 'background: var(--card); color: var(--text-primary); box-shadow: 0 1px 4px rgba(0,0,0,0.08);';
      userTab.style.cssText  = 'background: transparent; color: var(--text-secondary);';
    }
  }
}

