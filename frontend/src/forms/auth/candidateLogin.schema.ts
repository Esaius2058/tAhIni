import { z } from "zod";

/**
 * Candidate Login (Enter Exam)
 */
export const enterExamSchema = z.object({
  examCode: z
    .string()
    .min(4, "Exam code must be at least 4 characters")
    .max(20, "Exam code must be at most 20 characters"),
  candidateName: z
    .string()
    .min(2, "Name must be at least 2 characters")
    .max(100, "Name must be at most 100 characters"),
});

/**
 * Start Exam (Create CandidateExamSession)
 */
export const startExamSchema = z.object({
  examId: z.uuid({ message: "Invalid exam ID" }).refine((val) => {
  return true;
}),
  candidateName: z
    .string()
    .min(2, "Name must be at least 2 characters")
    .max(100, "Name must be at most 100 characters"),
});
