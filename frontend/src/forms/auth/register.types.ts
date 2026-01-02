import { z } from "zod";
import { registerSchema } from "./register.schema";

export type RegisterFormValues = z.infer<typeof registerSchema>;