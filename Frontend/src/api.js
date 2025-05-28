const API_BASE = import.meta.env.VITE_API_URL;

export async function checkAuth() {
  const res = await fetch(`${API_BASE}/api/account/check-auth`, {
    credentials: 'include',
  });
  return await res.json();
}

export async function createPost(data) {
  const res = await fetch(`${API_BASE}/api/blog/createposts`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
    credentials: 'include',
  });
  return await res.json();
}
