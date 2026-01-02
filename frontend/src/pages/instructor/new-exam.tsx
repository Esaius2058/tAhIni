"use client";
import { useState } from "react";
import { toast } from "sonner";
import { useAuth } from "../../auth/AuthContext";
import { createExamApi } from "../../api/exam";
import { ExamCreate } from "../../types/exam";

export default function NewExamPage() {
  const [title, setTitle] = useState("");
  const [subject, setSubject] = useState("");
  const [course, setCourse] = useState("");
  const [semester, setSemester] = useState("");
  const [duration, setDuration] = useState("");
  const [passmark, setPassmark] = useState(40)

  const { user } = useAuth();
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const examData: ExamCreate = {
      title,
      subject,
      author_id: user ? user.id : "author",
      course_id: course,
      pass_mark: passmark,
      semester_id: semester,
      duration: duration,
    };

    const exam = await createExamApi(examData);
    return exam ? toast.success("Exam created successfully") : toast.error("Error creating exam");
  };

  return (
    <div className="flex flex-col items-center justify-center">
      <h1 className="text-2xl font-bold mb-6">Create New Exam</h1>

      <form onSubmit={handleSubmit} className="space-y-7 max-w-md">
        <div className="flex flex-col gap-5">
          <div>
            <label className="block text-sm font-medium">Exam Title</label>
            <input
              type="text"
              className="mt-1 md:w-[400px] border px-3 py-2 rounded"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium">Subject</label>
            <input
              type="text"
              className="mt-1 md:w-[400px] border px-3 py-2 rounded"
              value={subject}
              onChange={(e) => setSubject(e.target.value)}
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium">Course Code</label>
            <input
              type="text"
              className="mt-1 md:w-[400px] border px-3 py-2 rounded"
              value={course}
              onChange={(e) => setCourse(e.target.value)}
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium">Semester</label>
            <input
              type="text"
              className="mt-1 md:w-[400px] border px-3 py-2 rounded"
              value={semester}
              onChange={(e) => setSemester(e.target.value)}
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium">Pass Mark</label>
            <input
              type="text"
              className="mt-1 md:w-[400px] border px-3 py-2 rounded"
              value={passmark}
              onChange={(e) => setPassmark(Number(e.target.value))}
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium">Duration</label>
            <input
              type="text"
              className="mt-1 md:w-[400px] border px-3 py-2 rounded"
              value={duration}
              onChange={(e) => setDuration(e.target.value)}
              required
            />
          </div>
        </div>
        <button
          type="submit"
          className="px-4 py-2 w-[180px] rounded text-white"
        >
          Create
        </button>
      </form>
    </div>
  );
}
