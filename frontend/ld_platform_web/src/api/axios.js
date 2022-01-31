import axios from "axios";
import { Routes } from "../routes";

const LdAxios = axios.create({
  baseURL: process.env.REACT_APP_BASE_URL,
  withCredentials: true,
  headers: {
    "content-type": "application/json"
  }
});

// uses http-only JWT cookie for authorization
LdAxios.interceptors.response.use(
  res => res,
  e => {
    if (e && !axios.isCancel(e)) {
      const res = e.response;
      if (!res) throw e;

      if (res.status === 401) {
        // redirect to Login page
        window.location.href = `/#${Routes.Login.path}`;
        return;
      }
    }
    throw {
      status: e.response.status,
      messages: e.response.data.data
    };
  }
);

export default LdAxios;
