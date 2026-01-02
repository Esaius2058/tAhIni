"use client";
import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { getExamByIdApi } from "../../api/exam";
import { ExamRead } from "../../types/exam";

export default function SingleExamPage() {
  const [exam, setExam] = useState<ExamRead | null>(null);
  const [loading, setLoading] = useState(true);

  const { id } = useParams<{ id: string }>(); 

  useEffect(() => {
    const load = async () => {
      try {
        const data = await getExamByIdApi(id as string);
        setExam(data);
      } catch (e) {
        console.error(e);
      } finally {
        setLoading(false);
      }
    };
    load();
  }, [id]);

  if (loading) return <p>Loading exam...</p>;
  if (!exam) return <p>Exam not found.</p>;

  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-bold">{exam.title}</h1>
      <p className="text-gray-600">
        Created: {new Date(exam.created_at).toLocaleString()}
      </p>

      <div className="p-4">
        <p className="text-gray-700">{exam.course.name} ({exam.course.code})</p>
        <p className="text-gray-700">Instructor: {exam.author.name}</p>
        <p className="text-gray-700">Passmark: {exam.pass_mark}</p>
        <p className="text-gray-700">Duration: {exam.duration}</p>
      </div>
    </div>
  )
};