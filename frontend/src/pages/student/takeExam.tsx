import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { getSessionQuestions } from "@/api/candidateExam";
import { Timer } from "@/components/exam/Timer";
import { submitExam } from "@/api/candidateExam";
import { getCandidateExamSession } from "@/api/candidateExam";
import QuestionRenderer from "@/components/student/QuestionRenderer";
import { Spinner } from "@/components/ui/spinner";
import { ChevronLeft, ChevronRight } from "lucide-react";
import { Question } from "@/types/question";
import { toast } from "sonner";

export default function TakeExamPage() {
  const navigate = useNavigate();

  const [loading, setLoading] = useState(true);
  const [session, setSession] = useState<any>(null);
  const [questions, setQuestions] = useState<Question[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);

  useEffect(() => {
    async function bootstrap() {
      try {
        const sessionData = await getCandidateExamSession();
        const questionsData = await getSessionQuestions();
        setSession(sessionData);
        setQuestions(questionsData);
        setLoading(false);
      } catch {
        toast.error("Error resolving exam session details");
        const timerId = setTimeout(() => {
          navigate(`exams/${ sessionStorage.getItem("examId")}/start`);
        }, 3000);

        return () => {
          clearTimeout(timerId);
        };
      }
    }

    bootstrap();
  }, []);

  const handleSubmit = async () => {
    navigate(`/exams/${sessionStorage.getItem("examID")}/submit`);
  };

  if (loading) return <Spinner />;

  const currentQuestion = questions[currentIndex];

  return (
    <div className="exam-page">
      <Timer
        endsAt={session.ends_at}
        onTimeUp={async () => {
          await submitExam();
          const examId = sessionStorage.getItem("examId");
          navigate(`/exams/${examId}/submit`);
        }}
      />

      <QuestionRenderer question={currentQuestion} sessionId={sessionStorage.getItem("sessionId")} />

      <div className="navigation-controls">
        <button
          disabled={currentIndex === 0}
          onClick={() => setCurrentIndex((i) => i - 1)}
        >
          <ChevronLeft />
        </button>

        <button
          disabled={currentIndex === questions.length - 1}
          onClick={() => setCurrentIndex((i) => i + 1)}
        >
          <ChevronRight />
        </button>
      </div>

      <button className="submit-btn" onClick={handleSubmit}>
        Submit Exam
      </button>
    </div>
  );
}
