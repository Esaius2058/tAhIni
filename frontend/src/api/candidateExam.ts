import examApi from "@/lib/axiosExamApi";
import {
  EnterExamPayload,
  StartExamPayload,
  EnterExamResponse,
  StartExamResponse,
} from "../forms/auth/candidateLogin.types";
import { CandidateExamSession } from "@/types/candidateSession";
import { Question } from "@/types/question";
import {
  AutosavePayload,
  AutosaveResponse,
  ExamSessionSummary,
} from "@/types/examSession";

/**
 * Enter exam using exam code + candidate name
 */
const enterExamApi = async (
  payload: EnterExamPayload
): Promise<EnterExamResponse> => {
  try {
    const response = await examApi.post<EnterExamResponse>(
      "/candidate/exam/enter",
      {
        exam_code: payload.examCode,
        candidate_name: payload.candidateName,
      }
    );

    return response.data;
  } catch (error) {
    console.error("Enter exam error:", error);
    throw error;
  }
};

/**
 * Start exam (create / restore CandidateExamSession)
 */
const startExamApi = async (
  payload: StartExamPayload
): Promise<StartExamResponse> => {
  try {
    const response = await examApi.post<StartExamResponse>(
      "/candidate/exam/start",
      {
        exam_id: payload.examId,
        candidate_name: payload.candidateName,
      }
    );

    return response.data;
  } catch (error) {
    console.error("Start exam error:", error);
    throw error;
  }
};

const getCandidateExamSession = async (): Promise<CandidateExamSession> => {
  try {
    const response = await examApi.get<CandidateExamSession>(
      "/candidate/exam-session/current"
    );
    return response.data;
  } catch (error) {
    console.error("Get candidate session error:", error);
    throw error;
  }
};

const getSessionQuestions = async (): Promise<Question[]> => {
  try {
    const response = await examApi.get<Question[]>(
      "/candidate/exam-session/questions"
    );
    return response.data;
  } catch (error) {
    console.error("Get session questions error:", error);
    throw error;
  }
};

const autosaveAnswer = async (
  payload: AutosavePayload
): Promise<AutosaveResponse> => {
  try {
    const response = await examApi.post<AutosaveResponse>(
      "/candidate/exam-session/autosave",
      {
        question_id: payload.question_id,
        answer: payload.answer,
      }
    );

    return response.data;
  } catch (error) {
    console.error("Autosave answer error:", error);
    throw error;
  }
};

const submitExam = async (): Promise<string> => {
  try {
    const response = await examApi.post<string>("/candidate/exam-session/submit");
    return response.data;
  } catch (error) {
    console.error("Submit exam error:", error);
    throw error;
  }
};

const getSubmissionSummary = async (): Promise<ExamSessionSummary> => {
  try {
    const response = await examApi.get<ExamSessionSummary>("/candidate/exam-session/summary");
    return response.data;
  } catch (error) {
    console.error("Submit exam error:", error);
    throw error;
  }
};

export {
  enterExamApi,
  startExamApi,
  getCandidateExamSession,
  getSessionQuestions,
  autosaveAnswer,
  submitExam,
  getSubmissionSummary,
};
