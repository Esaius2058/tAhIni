// lib/examApi.ts
import axios from "axios";

const examApi = axios.create({
  baseURL: "http://localhost:8000/api/v1",
});

export const setAuthToken = (token: string | null) => {
  if (token) {
    examApi.defaults.headers.common["Authorization"] = `Bearer ${token}`;
  } else {
    delete examApi.defaults.headers.common["Authorization"];
  }
}

examApi.interceptors.request.use((config) => {
  const token = localStorage.getItem("tAhIni_exam_token");

  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
});

examApi.interceptors.response.use(
  (res) => res,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem("tAhIni_exam_token");
      window.location.href = "/exams/candidate/entry";
    }
    return Promise.reject(error);
  }
);

export default examApi;
