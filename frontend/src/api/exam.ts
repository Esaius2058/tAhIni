// src/api/exam.ts
import api from "../lib/axiosApi";
import {
  ExamCreate,
  ExamRead,
  ExamUpdate,
  ExamStatsRead,
  ExamResultsRead,
} from "../types/exam";
import { Question, QuestionRead } from "../types/question";

export const createExamApi = async (data: ExamCreate) => {
  try {
    const response = await api.post<ExamRead>("/exam/new", data);
    return response.data;
  } catch (error) {
    console.error("Create exam error:", error);
    throw error;
  }
};

export const getExamByIdApi = async (id: string) => {
  try {
    const response = await api.get<ExamRead>(`/exam/${id}`);
    return response.data;
  } catch (error) {
    console.error("Fetch exam error:", error);
    throw error;
  }
};

export const getQuestionsInExamApi = async (examId: string) => {
  try {
    const response = await api.get<QuestionRead[]>(
      `/exam/questions/${examId}`
    );
    return response.data;
  } catch (error) {
    console.error("Fetch questions error:", error);
    throw error;
  }
};

export const getExamsByCourseApi = async (courseId: string, semesterId: string) => {
  try {
    const response = await api.get<ExamRead[]>(
      `/exam/course/${courseId}/${semesterId}`
    );
    return response.data;
  } catch (error) {
    console.error("Fetch exams for course error:", error);
    throw error;
  }
};

export const getExamsByInstructor = async (instructorId: string) => {
  try{
    const response = await api.get<ExamRead[]>(
      `/exam/instructor/${instructorId}`
    );
    return response.data;
  } catch (error) {
    console.error("Failed to fetch exams by ", instructorId, ": ",error);
    throw error;
  }
}

export const getQuestionInExamApi = async (examId: string, questionId: string) => {
  try {
    const response = await api.get<QuestionRead>(
      `/exam/${examId}/questions/${questionId}`
    );
    return response.data;
  } catch (error) {
    console.error("Fetch question error:", error);
    throw error;
  }
};

export const addQuestionToExamApi = async (examId: string, questionData: Question): Promise<Question> => {
  try {
    const response = await api.post<Question>(
      `/exam/${examId}/question/add`, // Matches your backend route
      questionData
    );
    return response.data
  } catch (error) {
    console.error("Failed to add question to exam:", error);
    throw error;
  }
};

export const deleteQuestionFromExamApi = async (examId: string, questionId: string) => {
  try {
    await api.delete(`/exam/${examId}/questions/${questionId}`);
  } catch (error) {
    console.error("Delete question error:", error);
    throw error;
  }
};

export const updateExamApi = async (examId: string, data: ExamUpdate) => {
  try {
    const response = await api.patch(`/exam/${examId}`, data);
    return response.data;
  } catch (error) {
    console.error("Update exam error:", error);
    throw error;
  }
};

export const deleteExamApi = async (examId: string) => {
  try {
    await api.delete(`/exam/${examId}`);
  } catch (error) {
    console.error("Delete exam error:", error);
    throw error;
  }
};

export const startExamApi = async (examId: string) => {
  try {
    const response = await api.post(`/exam/${examId}/start`);
    return response.data;
  } catch (error) {
    console.error("Start exam error:", error);
    throw error;
  }
};

export const getExamStatisticsApi = async (examId: string) => {
  try {
    const response = await api.get<ExamStatsRead>(
      `/exam/${examId}/stats`
    );
    return response.data;
  } catch (error) {
    console.error("Exam stats error:", error);
    throw error;
  }
};

export const getExamResultsApi = async (examId: string, userId: string) => {
  try {
    const response = await api.get<ExamResultsRead>(
      `/exam/${examId}/results/${userId}`
    );
    return response.data;
  } catch (error) {
    console.error("Exam results error:", error);
    throw error;
  }
};

