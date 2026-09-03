import {
  MapContainer,
  Marker,
  Popup,
  TileLayer,
} from "react-leaflet";
import { useEffect, useState } from "react";
import { LatLngBounds } from "leaflet";

import "leaflet/dist/leaflet.css";
import { getIncidents } from "../services/incidentService";
import { getResponders } from "../services/responderService";
import type { Incident } from "../types/incident";
import type { Responder } from "../types/responder";

const DEFAULT_CENTER: [number, number] = [18.5204, 73.8567];

function getPriorityLabel(priority: Incident["priority"]) {
  switch (priority) {
    case "CRITICAL":
      return "CRITICAL";
    case "HIGH":
      return "HIGH";
    case "MEDIUM":
      return "MEDIUM";
    case "LOW":
      return "LOW";
    default:
      return priority;
  }
}

function MapView() {
  const [incidents, setIncidents] = useState<Incident[]>([]);
  const [responders, setResponders] = useState<Responder[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadMapData() {
      try {
        const [incidentData, responderData] = await Promise.all([
          getIncidents(),
          getResponders(),
        ]);
        setIncidents(incidentData);
        setResponders(responderData);
      } catch (err) {
        console.error(err);
        setError("Unable to load map data.");
      } finally {
        setLoading(false);
      }
    }

    loadMapData();
  }, []);

  const bounds =
    incidents.length > 0
      ? new LatLngBounds(
          incidents.map((incident) => [
            incident.latitude,
            incident.longitude,
          ])
        )
      : undefined;

  return (
    <MapContainer
      center={DEFAULT_CENTER}
      zoom={13}
      scrollWheelZoom={true}
      bounds={bounds}
      className="map"
    >
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      {incidents.map((incident) => (
        <Marker
          key={incident.id}
          position={[incident.latitude, incident.longitude]}
        >
          <Popup>
            <strong>{incident.title}</strong>
            <br />
            Priority: {getPriorityLabel(incident.priority)}
            <br />
            Status: {incident.status}
            <br />
            Incident ID: #{incident.id}
          </Popup>
        </Marker>
      ))}
      {responders.map((responder) => {
        if (responder.latitude === null || responder.longitude === null) {
          return null;
        }

        return (
          <Marker
            key={`responder-${responder.id}`}
            position={[responder.latitude, responder.longitude]}
          >
            <Popup>
              <strong>{responder.name}</strong>
              <br />
              Type: {responder.responder_type}
              <br />
              Status: {" "}
              <strong>{responder.status}</strong>
              <br />
              ID: {responder.id}
            </Popup>
          </Marker>
        );
      })}
      {loading && <div className="map-message">Loading incidents...</div>}
      {error && <div className="map-message">{error}</div>}
    </MapContainer>
  );
}

export default MapView;