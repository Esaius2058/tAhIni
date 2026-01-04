import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { getCandidateExamSession, startExamApi } from "@/api/candidateExam";
import ExamHeader from "@/components/exam/ExamHeader";
import ExamRules from "@/components/exam/ExamRules";
import { setAuthToken } from "@/lib/axiosExamApi"; //from examApi not the app api
import { Spinner } from "@/components/ui/spinner";
import { toast } from "sonner";

export default function ExamInstructionsPage() {
  const navigate = useNavigate();

  const [loading, setLoading] = useState(true);
  const [session, setSession] = useState(null);
  const [starting, setStarting] = useState(false);

  useEffect(() => {
    async function loadSession() {
      try {
        const data = await getCandidateExamSession();
        if (data.status == "locked") {
          navigate(`/exams/${ sessionStorage.getItem("examId")}/attempt-locked`);
          return;
        }

        setSession(data);
        setLoading(false);
      } catch (err: any) {
        toast.error(err.response?.data?.detail || "Error trying to get exam")
        const timerId = setTimeout(() => {
          navigate(`exams/${ sessionStorage.getItem("examId")}/start`);
        }, 3000)
        return () => {
          clearTimeout(timerId);
        };
      }
    }

    loadSession();
  }, []);

  const startExam = async () => {
    if (!session) return;
    setStarting(true);
    const examId = sessionStorage.getItem("examId");
    const candidateName = sessionStorage.getItem("candidateName");
    const data = await startExamApi({ examId, candidateName });

    sessionStorage.setItem("endsAt", data.ends_at);
    localStorage.setItem("tAhIni_exam_token", data.token);
    setAuthToken(data.token);
    sessionStorage.setItem("candidateExamToken", data.token);
    sessionStorage.setItem("sessionId", data.session_id);
    sessionStorage.setItem("candidateRef", data.candidate_ref);
    setStarting(false);
    navigate(`/student/exam/${data.session_id}`);
  };

  if (loading) return <Spinner /> + "Loading Exam Details";

  return (
    <div className="instructions-container">
      <ExamHeader />
      <ExamRules />
      <button onClick={startExam}>
        {starting ? <Spinner /> : "Start Exam"}
      </button>
    </div>
  );
}
