import { json } from "react-router-dom";
import { type ErrorType, type contentType, type endpoint, type methods, type OAuthToken, type OAuthProvider, type BearerType } from "./types";
import {parseStream} from "./functions";

export const BASE_URL = "http://127.0.0.1:8000/";

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

export async function fetch_raw(
  endpoint: endpoint,
  auth: boolean = false,
  method: methods,
  type?: contentType,
  bearer?: BearerType,
  errorCallback?: (e: ErrorType) => any,
  finallyCallback?: () => any,
  body?: BodyInit,
) {
  let headers: HeadersInit = {};
  if (type) {
    headers["Content-Type"] = type;
  }
  if (auth) {
    let token;
    if (bearer === 'access_token') {
      token = getOAuth().identity;
      headers["Authorization"] = `Bearer ${token}`;
    } else if (bearer === 'alt_token') {
      token = getToken();
      headers["Authorization"] = `Bearer ${token}`;
    }
    if (!token) {
      throw json({ message: "No token" }, { status: 401 });
    }
  }
  let response;
  try {
    response = await fetch(BASE_URL + endpoint, {
      method,
      headers,
      body,
    });
  if (!response.ok) {
    let message = response.statusText || "Something went wrong";
    throw json({}, { status: response.status, statusText: message})
  }
  return response;
  } catch (e) {
    response?.body?.getReader().read().then((v) => (v.value ? console.log(new TextDecoder().decode(v.value)) : null));
    console.log(e);
    console.log("Error in fetch");
    const status = (e as ErrorType).status || 500;
    let statusText = (e as ErrorType).statusText || "Connection refused";
    if (status === 401 || status === 422 || status === 403) {
      clearToken()
    };
    if (errorCallback) errorCallback({ status, statusText });
    throw json({}, { status: status, statusText: statusText });
  } finally {
    if (finallyCallback) finallyCallback();
  }
}

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
  const resp = await (await fetch_raw(endpoint, auth, method, type, bearer, errorCallback, finallyCallback, body)).json();
  if (thenCallback) return thenCallback(resp);
  return resp;
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

export async function* post_stream(
  endpoint: endpoint,
  auth: boolean = true,
  body: BodyInit,
  type?: contentType,
): AsyncGenerator<Array<string | any>, void, unknown>{
  const response = await fetch_raw(endpoint, auth, "POST", type, "alt_token", undefined, undefined, body);
  
  if (!response.ok) {
    throw new Error("Failed to fetch stream data");
  }
  
  const reader = response.body!.getReader();
  while (true) {
    const { done, value } = await reader.read();
    
    if (done) {
      break;
    }
    
    let text = new TextDecoder().decode(value);
    // remove whitespace
    text = text.trim();
    if (!text) {continue;}
    const parsed_stream = parseStream(text);
    yield parsed_stream;
  }
}

export function put(endpoint: endpoint, body: object) {
  return fetch_(endpoint, true, "PUT", "application/json",  "alt_token", undefined, undefined, undefined, JSON.stringify(body));
};

export function del(endpoint: endpoint) {
  return fetch_(endpoint, true, "DELETE", "application/json", "alt_token");
};