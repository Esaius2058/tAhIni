import {z} from "zod";

export const registerSchema = z.object({
    name: z.string().trim(),
    email: z.email().trim(),
    password: z.string().min(6),
    confirmPassword: z.string().min(6)
});