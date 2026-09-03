import axios from "axios";
import type { Responder } from "../types/responder";

const API_BASE_URL = "http://127.0.0.1:8002";

const api = axios.create({
  baseURL: API_BASE_URL,
});

export async function getResponders(): Promise<Responder[]> {
  const response = await api.get<{ responders: Responder[] }>("/responders");

  return response.data.responders;
}
