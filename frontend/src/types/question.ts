export type QuestionType = "mcq" | "essay" | "file_upload" | "code" | "numerical" | "true_false" | "short_answer" | "multi_response";

export interface Answer {
  id: string;
  text: string;
  is_correct?: boolean;
}

export interface Question {
  id: string;
  type: QuestionType;
  text: string;
  options?: string[];
  constraints?: {
    allowedFileTypes?: string[];
    maxSizeMB?: number;
  };
  lockdownProfile: "strict" | "relaxed";
  difficulty?: string;
  tags?: string[];
  embedding?: number[]; 
  exam_id?: string;

  answers: Answer[];
}

export interface QuestionBase {
  text: string;
  tags: string[];
  type: QuestionType;
  difficulty?: string | null;
}

export interface QuestionCreate extends QuestionBase {}

export interface QuestionRead extends QuestionBase {
  id: string;
  created_at?: string | null; 
}

export interface QuestionSearchRequest {
  query: string;
  top_n?: number;
  difficulty?: string | null;
  tags?: string[] | null;
}

export interface QuestionUpdate {
  difficulty?: string | null;
  tags?: string[] | null;
  type?: QuestionType;
}

export interface BulkQuestionCreate {
  questions: QuestionCreate[];
}

export interface BulkQuestionResponse {
  message: string;
  questions: QuestionRead[];
}

export interface TagRequest {
  tags: string[];
}