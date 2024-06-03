import { json } from "react-router-dom";
import type { ErrorType, endpoint, methods } from "./types";

const BASE_URL = "http://127.0.0.1:5000/";

export function saveToken(token: string) {
  localStorage.setItem("token", token);
};

export function getToken() {
  return localStorage.getItem("token");
};

export function clearToken() {
  localStorage.removeItem("token");
};

async function fetch_(
  endpoint: endpoint,
  auth: boolean = false,
  method: methods,
  body?: BodyInit
) {
  let headers: HeadersInit = {
    "Content-Type": "application/json",
  };
  if (auth) {
    const token = getToken();
    if (!token) {
      throw json({ message: "No token" }, { status: 401 });
    }
    headers["Authorization"] = `Bearer ${token}`;
  }
  try {
    const response = await fetch(BASE_URL + endpoint, {
      method,
      headers,
      body,
    });
  if (!response.ok) {
    let message = response.statusText || "Something went wrong";
    throw json({}, { status: response.status, statusText: message})
  }
  return await response.json();
  } catch (e) {
    const status = (e as ErrorType).status || 500;
    let statusText = (e as ErrorType).statusText || "Connection refused";
    if (status === 401) {
      clearToken()
      statusText = "Invalid email or password";
    };
    throw json({}, { status: status, statusText: statusText });
  }
};

export function get(endpoint: endpoint) {
  return fetch_(endpoint, true, "GET");
};

export function post(
  endpoint: endpoint,
  auth: boolean = false,
  body: object
) {
  return fetch_(endpoint, auth, "POST", JSON.stringify(body));
};

export function put(endpoint: endpoint, body: object) {
  return fetch_(endpoint, true, "PUT", JSON.stringify(body));
};

export function del(endpoint: endpoint) {
  return fetch_(endpoint, true, "DELETE");
};