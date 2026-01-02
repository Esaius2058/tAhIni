export type UserType = "student" | "instructor" | "admin";

export interface LoginUserRequest {
  email: string;
  password: string;
}

export interface RegisterUserRequest {
  name: string;
  email: string;
  password: string;
  type?: UserType;
}   

export interface User {
  id: string;
  name: string;
  email: string;
  type: UserType;
  created_at?: string; 
}

export interface LoginResponse {
  access_token: string;
  token_type: "bearer";
  user: User;
}
