import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { ExamSessionSummary } from "@/types/examSession";
import {
  submitExam,
  getCandidateExamSession,
  getSubmissionSummary,
} from "@/api/candidateExam";
import { Spinner } from "@/components/ui/spinner";
import { toast } from "sonner";

export default function SubmitExamPage() {
  const navigate = useNavigate();

  const [loading, setLoading] = useState(true);
  const [summary, setSummary] = useState<ExamSessionSummary>(null);
  const [submitting, setSubmitting] = useState(false);
  const [session, setSession] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadSession() {
      try {
        const [sessionData, summaryData] = await Promise.all([
          getCandidateExamSession(),
          getSubmissionSummary(),
        ]);

        if (sessionData.submitted_at) {
          navigate(`/exams/${sessionData.exam_id}/completed`);
          return;
        }

        setSession(sessionData);
        setSummary(summaryData);
      } catch (err: any) {
        toast.error(err.response?.data?.detail || "Error submitting exam. Log in and try again")
        const timerId = setTimeout(() => {
          navigate(`exams/${ sessionStorage.getItem("examId")}/start`);
        }, 2000)

        return () => {
          clearTimeout(timerId);
        };
      } finally {
        setLoading(false);
      }
    }

    loadSession();
  }, [navigate]);

  const handleSubmit = async () => {
    if (!session || submitting) return;

    setSubmitting(true);
    setError(null);

    try {
      await submitExam();
      navigate(`/exams/${sessionStorage.getItem("examId")}/completed`);
    } catch (err: any) {
      toast.error(err.response?.data?.detail || "Error submitting exam. Contact the instructor")
      setSubmitting(false);
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) return <div>Finalizing session…</div>;

  return (
    <div className="max-w-xl mx-auto mt-16 p-6 border rounded">
      {summary && (
        <div className="mb-6 p-4 bg-gray-50 border rounded">
          <h2 className="text-sm font-semibold mb-2">Exam Summary</h2>

          <div className="flex justify-between text-sm">
            <span>Total questions</span>
            <span>{summary.total}</span>
          </div>

          <div className="flex justify-between text-sm text-green-700">
            <span>Answered</span>
            <span>{summary.answered}</span>
          </div>

          <div className="flex justify-between text-sm text-red-700">
            <span>Unanswered</span>
            <span>{summary.unanswered}</span>
          </div>
        </div>
      )}

      <p className="text-sm text-gray-600 mb-4">
        You are about to submit your exam. Once submitted:
      </p>

      <ul className="text-sm text-gray-600 list-disc pl-5 mb-6">
        <li>You cannot edit your answers</li>
        <li>The exam session will be locked</li>
        <li>Your submission will be graded</li>
      </ul>

      {error && <div className="mb-4 text-sm text-red-600">{error}</div>}

      <div className="flex gap-3">
        <button
          onClick={() => navigate(-1)}
          disabled={submitting}
          className="px-4 py-2 border rounded"
        >
          Go Back
        </button>

        <button
          onClick={handleSubmit}
          disabled={submitting}
          className="px-4 py-2 bg-red-600 text-white rounded"
        >
          {submitting ? <Spinner /> : "Submit Exam"}
        </button>
      </div>
    </div>
  );
}
