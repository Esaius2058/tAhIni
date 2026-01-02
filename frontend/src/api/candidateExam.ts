import api from "../lib/axios";
import {
  EnterExamPayload,
  StartExamPayload,
  EnterExamResponse,
  StartExamResponse,
} from "../forms/auth/candidateLogin.types";
import { CandidateSessionResponse } from "@/types/candidateSession";
import { Question } from "@/types/question";
import { AutosavePayload, AutosaveResponse } from "@/types/examSession";

/**
 * Enter exam using exam code + candidate name
 */
const enterExamApi = async (
  payload: EnterExamPayload
): Promise<EnterExamResponse> => {
  try {
    const response = await api.post<EnterExamResponse>(
      "/candidate/enter-exam",
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
    const response = await api.post<StartExamResponse>(
      "/candidate/start-exam",
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

const getCandidateExamSession = async (): Promise<CandidateSessionResponse> => {
  try {
    const response = await axios.get<CandidateSessionResponse>(
      "/candidate/session/current",
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("candidate_token")}`,
        },
      }
    );
    return response.data;
  } catch (error) {
    console.error("Get candidate session error:", error);
    throw error;
  }
};

const getSessionQuestions = async (sessionId: string): Promise<Question[]> => {
  try {
    const response = await axios.get<Question[]>(
      `/candidate/exam-sessions/${sessionId}/questions`,
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("candidate_token")}`,
        },
      }
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
    const res = await axios.post<AutosaveResponse>(
      '/exam-sessions/autosave',
      {
        question_id: payload.question_id,
        answer: payload.answer,
      }
    );

    return res.data;
  } catch (error) {
    console.error("Autosave answer error:", error);
    throw error;
  }
};

const submitExam = async (sessionId: string): Promise<void> => {
  try {
    await axios.post(`/exam-sessions/${sessionId}/submit`);
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
};
