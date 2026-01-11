import { createContext, useContext, useState, useEffect, ReactNode } from "react";
import { ExamRead } from "@/types/exam";
import { getExamsByInstructor } from "@/api/exam";

interface ExamContextType {
  exams: ExamRead[];
  loading: boolean;
  refreshExams: () => Promise<void>;
}

const ExamContext = createContext<ExamContextType | undefined>(undefined);

export function ExamProvider({ children, instructorId }: { children: ReactNode; instructorId: string }) {
  const [exams, setExams] = useState<ExamRead[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchExams = async () => {
    if (!instructorId) return;
    try {
      setLoading(true);
      const data = await getExamsByInstructor(instructorId);
      setExams(data);
    } catch (error) {
      console.error("Failed to load exams", error);
    } finally {
      setLoading(false);
    }
  };

  // Automatically fetch when the provider mounts or instructorId changes
  useEffect(() => {
    fetchExams();
  }, [instructorId]);

  return (
    <ExamContext.Provider value={{ exams, loading, refreshExams: fetchExams }}>
      {children}
    </ExamContext.Provider>
  );
}

// Custom hook for easy access
export function useExams() {
  const context = useContext(ExamContext);
  if (!context) {
    throw new Error("useExams must be used within an ExamProvider");
  }
  return context;
}