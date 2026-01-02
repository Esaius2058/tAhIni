export interface StartExamRequest {
  exam_id: string;
  candidate_name: string;
}

export interface StartExamResponse {
  access_token: string;
  session_id: string;
  candidate_ref: string;
  exam_id: string;
  ends_at: string;
  status: "IN_PROGRESS";
}

export interface ExamTimerProps {
  endsAt: string; // ISO string from backend
  onTimeUp: () => void;
}

export interface AutosavePayload {
  question_id: string;
  answer: string;
}

export interface AutosaveResponse {
  status: "saved";
}