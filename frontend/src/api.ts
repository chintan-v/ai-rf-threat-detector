const API_BASE_URL =
  import.meta.env.VITE_API_URL ?? "http://127.0.0.1:8000";

export async function getSignal() {
  const response = await fetch(`${API_BASE_URL}/api/signal`);

  if (!response.ok) {
    throw new Error("Failed to fetch signal data");
  }

  return response.json();
}