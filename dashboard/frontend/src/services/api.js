import axios from "axios";

const API_BASE_URL =
  process.env.REACT_APP_API_URL || "http://localhost:5000/api";

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

export const fetchPrices = async (startDate, endDate) => {
  const params = {};
  if (startDate) params.start_date = startDate;
  if (endDate) params.end_date = endDate;

  const response = await api.get("/prices", { params });
  return response.data;
};

export const fetchEvents = async (startDate, endDate, eventType) => {
  const params = {};
  if (startDate) params.start_date = startDate;
  if (endDate) params.end_date = endDate;
  if (eventType) params.event_type = eventType;

  const response = await api.get("/events", { params });
  return response.data;
};

export const fetchChangepoint = async () => {
  const response = await api.get("/changepoint");
  return response.data;
};

export const fetchStatistics = async (startDate, endDate) => {
  const params = {};
  if (startDate) params.start_date = startDate;
  if (endDate) params.end_date = endDate;

  const response = await api.get("/statistics", { params });
  return response.data;
};

export const fetchEventTypes = async () => {
  const response = await api.get("/event-types");
  return response.data;
};

export const fetchDateRange = async () => {
  const response = await api.get("/date-range");
  return response.data;
};

export const checkHealth = async () => {
  const response = await api.get("/health");
  return response.data;
};

export default api;
