import axios from 'axios';

const api = axios.create({
    baseURL: "http://localhost:8000/api/v1",
    withCredentials: true,
});

export const setAuthToken = (token: string | null) => {
  if (token) {
    api.defaults.headers.common["Authorization"] = `Bearer ${token}`;
  } else {
    delete api.defaults.headers.common["Authorization"];
  }
}

api.interceptors.request.use((config) => {
    if (!config.headers) config.headers = {};

    const token = localStorage.getItem("tAhIni_token");

    if (token){
        config.headers.Authorization = `Bearer ${token}`;
        console.log("Token: ", config.headers.Authorization)
    }

    return config;
});

api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response?.status === 401){
            localStorage.removeItem("tAhIni_token");
            window.location.href = "/login"
        }

        return Promise.reject(error);
    }
);

export default api;