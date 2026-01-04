export type CandidateExamSession = {
  id: string;
  exam_id: string;

  candidate_name: string;
  candidate_ref?: string | null;

  started_at: string;   // ISO
  ends_at: string;      // ISO
  submitted_at?: string | null;

  status:"not_started" | "in_progress" | "submitted" | "locked" | "expired" | "completed";
};
