export type IncidentPriority =
  | "LOW"
  | "MEDIUM"
  | "HIGH"
  | "CRITICAL";

export type IncidentStatus =
  | "CREATED"
  | "SEARCHING"
  | "ASSIGNED"
  | "ACCEPTED"
  | "EN_ROUTE"
  | "ON_SCENE"
  | "RESOLVED";

export interface Incident {
  id: number;
  title: string;
  description: string | null;
  priority: IncidentPriority;
  status: IncidentStatus;
  latitude: number;
  longitude: number;
  created_at: string;
  updated_at: string;
}
