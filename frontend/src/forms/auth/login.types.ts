import { z } from "zod";
import { loginSchema } from "./login.schema";

export type LoginFormValues = z.infer<typeof loginSchema>;