import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getCandidateExamSession, getSubmissionSummary } from "@/api/candidateExam";
import { ExamSessionSummary } from "@/types/examSession";
import { Spinner } from "@/components/ui/spinner";

export default function LockedAttempt() {
  const navigate = useNavigate();
  const [summary, setSummary] = useState<ExamSessionSummary | null>(null);
  const [loading, setLoading] = useState(true);
  const [submittedAt, setSubmittedAt] = useState(null);

  useEffect(() => {
    async function loadSummary() {
      try {
        const sessionId = sessionStorage.getItem("sessionId");
        if (!sessionId) {
          navigate("/login");
          return;
        }

        const submissionData = await getSubmissionSummary();
        const sessionData = await getCandidateExamSession();
        setSummary(submissionData);
        setSubmittedAt(sessionData.submitted_at);
      } catch {
        navigate("/login");
      } finally {
        setLoading(false);
      }
    }

    loadSummary();
  }, [navigate]);

  if (loading) {
    return (
      <div className="flex justify-center mt-24">
        <Spinner />
      </div>
    );
  }

  if (!summary) return null;

  return (
    <div className="max-w-xl mx-auto mt-16 p-6 border rounded">
      <h1 className="text-xl font-semibold mb-2 text-red-600">
        Exam Attempt Locked
      </h1>

      <p className="text-sm text-gray-600 mb-6">
        This exam has already been submitted. You can no longer edit or view
        questions.
      </p>

      <div className="space-y-3 text-sm">
        <div className="flex justify-between">
          <span>Total Questions</span>
          <span>{summary.total}</span>
        </div>

        <div className="flex justify-between">
          <span>Answered</span>
          <span>{summary.answered}</span>
        </div>

        <div className="flex justify-between">
          <span>Unanswered</span>
          <span>{summary.unanswered}</span>
        </div>

        {submittedAt && <div className="flex justify-between">
          <span>Submitted At</span>
          <span>
            {new Date(submittedAt).toLocaleString()}
          </span>
        </div>}
      </div>

      <div className="mt-8 flex gap-3">
        <button
          onClick={() => navigate("/exams/completed")}
          className="px-4 py-2 bg-gray-800 text-white rounded"
        >
          Continue
        </button>
      </div>
    </div>
  );
}
