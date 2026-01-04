import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getCandidateExamSession } from "@/api/candidateExam";
import { Spinner } from "@/components/ui/spinner";

export default function ExamCompletedPage() {
  const navigate = useNavigate();
  const [session, setSession] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadSession() {
      try {
        const data = await getCandidateExamSession();

        if (!data.submitted_at) {
          // Someone tried to jump here manually
          navigate("/student");
          return;
        }

        setSession(data);
      } catch {
        navigate("/student/login");
      } finally {
        setLoading(false);
      }
    }

    loadSession();
  }, [navigate]);

  if (loading) return <Spinner />;

  return (
    <div className="max-w-xl mx-auto mt-24 p-6 border rounded text-center">
      <h1 className="text-2xl font-semibold mb-3">
        Exam Submitted Successfully
      </h1>

      <p className="text-sm text-gray-600 mb-6">
        Thank you, {session.candidate_name}. Your responses have been recorded.
      </p>

      <div className="text-sm text-gray-700 space-y-2">
        <div>
          <strong>Exam:</strong> {session.exam.title}
        </div>
        <div>
          <strong>Submitted at:</strong>{" "}
          {new Date(session.submitted_at).toLocaleString()}
        </div>

        {session.score !== null && (
          <div>
            <strong>Score:</strong> {session.score}
          </div>
        )}
      </div>

      <p className="mt-6 text-xs text-gray-500">
        You may now close this window.
      </p>
    </div>
  );
}
