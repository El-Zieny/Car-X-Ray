// Shared authentication module
export async function getProfile() {
  const token = localStorage.getItem("jwt");
  if (!token) {
    console.log("No token found");
    return null;
  }

  console.log("Token found:", token.substring(0, 20) + "...");

  try {
    const response = await fetch(
      "https://backend-project1-production.up.railway.app/auth/me",
      {
        method: "GET",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );

    console.log("Auth response status:", response.status);
    const data = await response.json();
    console.log("Profile response (FULL):", JSON.stringify(data, null, 2));

    if (data.success || data.user || data.data) {
      return data;
    }
    return null;
  } catch (error) {
    console.error("Error fetching profile:", error);
    return null;
  }
}

export function extractUserName(user) {
  if (!user) return null;
  
  // Log the entire user object for debugging
  console.log("User object structure:", JSON.stringify(user, null, 2));
  
  // Try different possible response structures
  const possiblePaths = [
    { value: user.user?.name, path: "user.user.name" },
    { value: user.user?.profile?.name, path: "user.user.profile.name" },
    { value: user.data?.user?.name, path: "data.user.name" },
    { value: user.data?.name, path: "data.name" },
    { value: user.name, path: "name" },
    { value: user.profile?.name, path: "profile.name" },
  ];

  console.log("Checking paths for name:", possiblePaths);

  const found = possiblePaths.find(p => p.value && typeof p.value === 'string');
  
  if (found) {
    console.log(`Name found at path "${found.path}":`, found.value);
    const firstName = found.value.split(" ")[0];
    console.log("First name extracted:", firstName);
    return firstName;
  }

  console.log("No name found in any path");
  console.log("Available keys:", Object.keys(user || {}));
  return null;
}

export async function updateAuthUI() {
  console.log("=== UPDATING AUTH UI ===");
  const user = await getProfile();
  console.log("Final user object:", user);

  // Update user names
  if (user) {
    const firstName = extractUserName(user);
    const displayName = firstName || "User";

    const userNameMobile = document.getElementById("userNameMobile");
    const userNameDesktop = document.getElementById("userNameDesktop");

    if (userNameMobile) {
      userNameMobile.textContent = `Hi, ${displayName}`;
      console.log("Mobile user name set to:", `Hi, ${displayName}`);
    }

    if (userNameDesktop) {
      userNameDesktop.textContent = `Hi, ${displayName}`;
      console.log("Desktop user name set to:", `Hi, ${displayName}`);
    }
  }

  // Setup logout handlers
  function logout(e) {
    e.preventDefault();
    localStorage.removeItem("jwt");
    window.location.href = "index.html";
  }

  document.getElementById("logoutBtnMobile")?.addEventListener("click", logout);
  document.getElementById("logoutBtnDesktop")?.addEventListener("click", logout);
  console.log("=== AUTH UI UPDATE COMPLETE ===");
}
