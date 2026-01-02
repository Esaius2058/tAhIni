export interface CandidateSessionResponse {
  session: {
    id: string;
    status: "IN_PROGRESS" | "TIMED_OUT" | "SUBMITTED";
    started_at: string;
    ends_at: string;
  };
  exam: {
    id: string;
    title: string;
    duration_minutes: number;
  };
}
