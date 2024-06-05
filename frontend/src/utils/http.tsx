import { json } from "react-router-dom";
import type { ErrorType, contentType, endpoint, methods } from "./types";

export const BASE_URL = "http://127.0.0.1:5000/";

export function saveToken(token: string) {
  localStorage.setItem("token", token);
};

export function getToken() {
  return localStorage.getItem("token");
};

export function clearToken() {
  localStorage.removeItem("token");
};

export async function fetch_(
  endpoint: endpoint,
  auth: boolean = false,
  method: methods,
  type: contentType,
  thenCallback?: (jsonResp: any) => any,
  errorCallback?: (e: ErrorType) => any,
  finallyCallback?: () => any,
  body?: BodyInit,
) {
  let headers: HeadersInit = {
    "Content-Type": type,
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
  const jsonResp = await response.json();
  if (!thenCallback) return jsonResp;
  return thenCallback(jsonResp);
  } catch (e) {
    const status = (e as ErrorType).status || 500;
    let statusText = (e as ErrorType).statusText || "Connection refused";
    if (status === 401 || status === 422) {
      clearToken()
    };
    if (errorCallback) errorCallback({ status, statusText });
    throw json({}, { status: status, statusText: statusText });
  } finally {
    if (finallyCallback) finallyCallback();
  }
};

export function get(endpoint: endpoint) {
  return fetch_(endpoint, true, "GET", "application/json");
};

export function post(
  endpoint: endpoint,
  auth: boolean = false,
  body: object
) {
  return fetch_(endpoint, auth, "POST", "application/json", undefined, undefined, undefined, JSON.stringify(body));
};

export function put(endpoint: endpoint, body: object) {
  return fetch_(endpoint, true, "PUT", "application/json", undefined, undefined, undefined, JSON.stringify(body));
};

export function del(endpoint: endpoint) {
  return fetch_(endpoint, true, "DELETE", "application/json");
};