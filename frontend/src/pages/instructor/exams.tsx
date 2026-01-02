"use client";
import { Link, useParams } from "react-router-dom";
import { useAuth } from "@/auth/useAuth";
import { useEffect, useState } from "react";
import { getExamsByInstructor } from "../../api/exam";
import { ExamRead } from "../../types/exam";
import { toast } from "sonner";
import { Plus } from "lucide-react";

export default function InstructorExamListPage() {
  const [exams, setExams] = useState<ExamRead[]>([]);
  const [loading, setLoading] = useState(true);

  const { user } = useAuth();
  let { instructorId } = useParams();

  useEffect(() => {
    const load = async () => {
      console.log("Instructor ID: ", instructorId);
      try {
        instructorId = instructorId != null ? instructorId : user.id;
        const data = await getExamsByInstructor(instructorId);
        setExams(data);
      } catch (e) {
        console.error("Failed to load exams", e);
        toast.error("Failed to load exams");
      } finally {
        setLoading(false);
      }
    };

    load();
  }, []);

  if (loading) return <p>Loading exams...</p>;

  return (
    <div className="space-y-4">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold">Your Exams</h1>
        <Link
          to="/instructor/exams/new"
          className="px-2 py-2 rounded-full transition duration-300 ease-in-out hover:bg-gray-300 hover:text-white"
        >
          <Plus name="new exam"/>
        </Link>
      </div>

      {exams.length === 0 ? (
        <p>No exams yet.</p>
      ) : (
        <div className="space-y-3">
          {exams.map((exam) => (
            <Link
      key={exam.id} // Unique Exam ID is safer than Author ID
      to={`/instructor/exams/${exam.id}`}
      className="p-4 border rounded-lg block hover:bg-gray-50 transition"
    >
      <h3 className="font-semibold">{exam.title}</h3>
      <p className="text-gray-600 text-sm">
        {/* Safe date handling */}
        Created: {exam.created_at ? new Date(exam.created_at).toLocaleString() : 'N/A'}
      </p>
    </Link>
          ))}
        </div>
      )}
    </div>
  );
}
