import { json } from "react-router-dom";
import type { ErrorType, contentType, endpoint, methods, OAuthToken, OAuthProvider, BearerType } from "./types";

export const BASE_URL = "http://127.0.0.1:5000/";

export function saveToken(identity: string) {
  localStorage.setItem("token", identity);
};

export function getToken() {
  return localStorage.getItem("token");
};

export function clearToken() {
  localStorage.removeItem("token");
};

export function getOAuth(): OAuthToken {
  return JSON.parse(localStorage.getItem("oauth") ? localStorage.getItem("oauth")! : "{}");
}

export function saveOAuth(provider: OAuthProvider, identity: string) {
  localStorage.setItem("oauth", JSON.stringify({provider, identity}));
};

export function clearOAuth() {
  localStorage.removeItem("oauth");
};

export async function fetch_(
  endpoint: endpoint,
  auth: boolean = false,
  method: methods,
  type: contentType,
  bearer?: BearerType,
  thenCallback?: (jsonResp: any) => any,
  errorCallback?: (e: ErrorType) => any,
  finallyCallback?: () => any,
  body?: BodyInit,
) {
  let headers: HeadersInit = {
    "Content-Type": type,
  };
  if (auth) {
    let token;
    if (bearer === 'access_token') {
      token = getOAuth().identity;
    } else {
      token = getToken();
    }
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
    console.log(e);
    console.log("Error in fetch");
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
}

export function get(
  endpoint: endpoint,
  bearer: 'alt_token' | 'access_token'
  ) {
  return fetch_(endpoint, true, "GET", "application/json", bearer);
};

export function post(
  endpoint: endpoint,
  auth: boolean = false,
  body: object
) {
  return fetch_(endpoint, auth, "POST", "application/json", "alt_token", undefined, undefined, undefined, JSON.stringify(body));
};

export function put(endpoint: endpoint, body: object) {
  return fetch_(endpoint, true, "PUT", "application/json",  "alt_token", undefined, undefined, undefined, JSON.stringify(body));
};

export function del(endpoint: endpoint) {
  return fetch_(endpoint, true, "DELETE", "application/json", "alt_token");
};