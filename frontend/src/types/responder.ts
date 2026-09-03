export type ResponderType =
  | "POLICE"
  | "AMBULANCE"
  | "FIRE";

export type ResponderStatus =
  | "AVAILABLE"
  | "BUSY"
  | "OFFLINE";

export interface Responder {
  id: number;
  name: string;
  phone: string;
  responder_type: ResponderType;
  status: ResponderStatus;
  latitude: number | null;
  longitude: number | null;
  updated_at?: string | null;
}
