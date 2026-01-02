import { z } from "zod";
import {
  enterExamSchema,
  startExamSchema,
} from "../auth/candidateLogin.schema";

/**
 * Request types
 */
export type EnterExamPayload = z.infer<typeof enterExamSchema>;
export type StartExamPayload = z.infer<typeof startExamSchema>;

/**
 * API responses
 */
export interface EnterExamResponse {
  exam_id: string;
  title: string;
  duration_minutes: number;
}

export interface StartExamResponse {
  session_id: string;
  candidate_ref: string;
  token: string;
  ends_at: string | null;
}
