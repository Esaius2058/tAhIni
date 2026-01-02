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

export default function TakeExamPage() {
  const { sessionId } = useParams<{ sessionId: string }>();
  const navigate = useNavigate();

  const [loading, setLoading] = useState(true);
  const [session, setSession] = useState<any>(null);
  const [questions, setQuestions] = useState<Question[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);

  useEffect(() => {
    async function bootstrap() {
      try {
        const questionsData = await getSessionQuestions(sessionId!);

        const data = await getCandidateExamSession();
        setSession(data.session);
        setQuestions(questionsData);
        setLoading(false);
      } catch {
        navigate("/student/login");
      }
    }

    bootstrap();
  }, [sessionId]);

  const handleSubmit = async () => {
    await submitExam(sessionId!);
    navigate("/student/submitted");
  };

  if (loading) return <Spinner />;

  const currentQuestion = questions[currentIndex];

  return (
    <div className="exam-page">
      <Timer
        endsAt={session.ends_at}
        onTimeUp={async () => {
          await submitExam(session.id);
          navigate("/student/exam-submitted");
        }}
      />

      <QuestionRenderer question={currentQuestion} sessionId={sessionId!} />

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
