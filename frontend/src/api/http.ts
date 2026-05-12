export interface ApiRequestOptions extends RequestInit {
  auth?: boolean;
}

const API_BASE = import.meta.env.VITE_API_BASE_URL ?? "";

export async function apiRequest<T>(path: string, options: ApiRequestOptions = {}): Promise<T> {
  const headers = new Headers(options.headers);
  headers.set("Content-Type", "application/json");

  const token = localStorage.getItem("xhm_access_token");
  if (options.auth !== false && token) {
    headers.set("Authorization", `Bearer ${token}`);
  }

  const response = await fetch(`${API_BASE}${path}`, { ...options, headers });
  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(errorText || `Request failed with ${response.status}`);
  }

  return (await response.json()) as T;
}
