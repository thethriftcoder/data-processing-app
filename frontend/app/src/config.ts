export const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;
export const USER_NAME = import.meta.env.VITE_USER_NAME;
export const USER_PASSWORD = import.meta.env.VITE_USER_PASSWORD;

export interface ApiResponse<T> {
  data: T;
}

export const AUTH_HEADER = "Basic " + btoa(USER_NAME + ":" + USER_PASSWORD);
