import api from "../lib/axios";
import { LoginUserRequest, RegisterUserRequest } from "../types/auth";

const registerUserApi = async (userData: RegisterUserRequest) => {
    try{
        await api.post(`/auth/register`, userData);
    } catch(error){
        console.error("Registration error:", error);
        throw error;
    }
}

const loginUserApi = async (userData: LoginUserRequest, login: (userData: any, token: string) => void) => {
    try{
        const response = await api.post("/auth/login", userData) as any;
        const { access_token, user } = response.data;
        login(user, access_token);
        api.defaults.headers.common["Authorization"] = `Bearer ${access_token}`
        console.log("Logged in successfully: ", user);

        return response.data;
    } catch(error){
        console.error("Log in error:", error);
        throw error;
    }
}

export { registerUserApi, loginUserApi };