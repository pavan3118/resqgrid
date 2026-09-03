import axios from "axios";
import type { Incident } from "../types/incident";

const API_BASE_URL = "http://127.0.0.1:8002";

const api = axios.create({
  baseURL: API_BASE_URL,
});

export async function getIncidents(): Promise<Incident[]> {
  const response = await api.get<{ incidents: Incident[] }>("/incidents");

  return response.data.incidents;
}
