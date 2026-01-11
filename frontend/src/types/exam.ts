import { QuestionRead } from "./question";

export interface ExamBase {
  title: string;
  subject: string;
  author_id: string; 
  course_id: string;
  semester_id: string;
  duration: number; 
  pass_mark: number; 
}
export interface ExamCreate extends ExamBase {}
 
export interface ExamRead extends ExamBase {
  id: string;
  exam_code: string;
  created_at: string; 
  updated_at: string; 
  course: {
    name: string;
    code: string;
  };
  author: {
    name: string;
  };
  questions: QuestionRead[];
}

export interface ExamUpdate {
  subject?: string;
  title?: string;
  duration?: string;
  pass_mark?: number;
  course_id?: string;
  semester_id?: string;
}

export interface ExamStatsRead {
  exam_title: string;
  average_score: number; 
  pass_rate: number; 
}

export interface ExamResultsRead {
  title: string;
  subject: string;
  grader: string;
  score: number; 
}
