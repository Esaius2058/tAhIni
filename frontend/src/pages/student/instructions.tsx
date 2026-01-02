import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { getCandidateExamSession, startExamApi } from "@/api/candidateExam";
import ExamHeader from "@/components/exam/ExamHeader";
import ExamRules from "@/components/exam/ExamRules";
import { Spinner } from "@/components/ui/spinner";

export default function ExamInstructionsPage() {
  const navigate = useNavigate();

  const [loading, setLoading] = useState(true);
  const [exam, setExam] = useState(null);
  const [session, setSession] = useState(null);

  useEffect(() => {
    async function loadSession() {
      try {
        const data = await getCandidateExamSession();

        setSession(data.session);
        setLoading(false);
      } catch (err: any) {
        if (err.response?.status === 403) {
          navigate("/student/attempt-locked");
        } else {
          navigate("/login");
        }
      }
    }

    loadSession();
  }, []);

  const startExam = async () => {
    if(!session) return;
    const examId = sessionStorage.getItem("examId");
    const candidateName = sessionStorage.getItem("candidateName");
    const data = await startExamApi({examId, candidateName});

    sessionStorage.setItem("endsAt", data.ends_at);
    sessionStorage.setItem("endsAt", data.ends_at);
    navigate(`/student/exam/${data.session_id}`);
  };

  if (loading) return <Spinner />;

  return (
    <div className="instructions-container">
      <ExamHeader exam={exam} />
      <ExamRules />
      <button onClick={startExam}>Start Exam</button>
    </div>
  );
}
