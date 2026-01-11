import { useEffect, useState } from "react";
import { Plus, Pencil, Trash } from "lucide-react";
import { Question } from "../../types/question";
import { useExams } from "@/context/ExamContext";
import QuestionBuilder from "../../components/instructor/QuestionBuilder";
import { useParams } from "react-router-dom";
import { addQuestionToExamApi } from "@/api/exam";
import { toast } from "sonner";

export default function InstructorQuestionsPage() {
  const { id: examId } = useParams(); 
  const { exams } = useExams();
  const [loading, setLoading] = useState(true);
  const [questions, setQuestions] = useState<Question[]>([]);
  const [showBuilder, setShowBuilder] = useState(false);
  const [editingQuestion, setEditingQuestion] = useState<Partial<Question> | null>(null)

  useEffect(() => {
    setTimeout(() => {
      setLoading(false);
    }, 600);
  }, [examId]);

  const handleCreate = async (questionPayload: Question) => {
    try {
      const savedQuestion = await addQuestionToExamApi(questionPayload.exam_id!, questionPayload);
      setQuestions((prev) => [...prev, savedQuestion]);
    } catch (error) {
      console.error("Failed to create question", error);
      toast.error("Failed to save question. Please try again.");
      throw error;
    }
  };

  const handleUpdate = (updated: Question) => {
    setQuestions((prev) =>
      prev.map((q) => (q.id === updated.id ? updated : q))
    );
  };

  const handleDelete = (id: string) => {
    setQuestions((prev) => prev.filter((q) => q.id !== id));
  };

  const formatQuestionType = (type: string) => {
    const map: Record<string, string> = {
      true_false: "True / False",
      mcq: "MCQ",
      short_answer: "Short Answer",
      multi_response: "Multi Response"
    };
    return map[type] || type;
  }

  if (loading) return <div>Loading questions…</div>;

  return (
    <div className="w-full space-y-6 flex flex-col items-center">
      <div className="flex justify-between items-center w-full">
        <h1 className="text-xl font-semibold">Questions for Exam {examId}</h1>
        <button
          className="flex gap-2 items-center rounded-full px-3 py-2 hover:scale-110 bg-transparent text-gray-500 hover:bg-gray-100 hover:text-gray-500"
          onClick={() => {
            // 3. Pre-select the current exam ID when creating a new question
            setEditingQuestion({ exam_id: examId } as Question); 
            setShowBuilder(true);
          }}
        >
          <Plus size={18} />
        </button>
      </div>

      {/* QUESTIONS TABLE */}
      <div className="bg-white p-4 rounded w-full">
        <table className="w-full">
          <thead>
            <tr className="text-left border-b">
              <th className="py-2">Question</th>
              <th className="py-2">Type</th>
            </tr>
          </thead>
          <tbody>
            {questions.map((q) => (
              <tr key={q.id} className="text-left border-b hover:bg-gray-50">
                <td className="py-3 pr-4">
                    <p className="line-clamp-2 text-sm">{q.text}</p>
                </td>
                <td className="capitalize text-sm text-gray-600">{formatQuestionType(q.type)}</td>
                <td className="text-right">
                  <div className="flex gap-3 justify-end">
                    <button
                      onClick={() => {
                        setEditingQuestion(q);
                        setShowBuilder(true);
                      }}
                      className="bg-transparent text-black rounded-full hover:scale-110"
                    >
                      <Pencil size={18} />
                    </button>

                    <button
                      onClick={() => handleDelete(q.id)}
                      className="bg-transparent text-black rounded-full hover:scale-110"
                    >
                      <Trash size={18} />
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>

        {questions.length === 0 && (
          <div className="text-gray-500 text-center py-10 flex flex-col items-center gap-2">
            <p>No questions yet.</p>
            <button 
                onClick={() => { setEditingQuestion({ exam_id: examId } as Question); setShowBuilder(true); }}
                className=""
            >
                Add your first question
            </button>
          </div>
        )}
      </div>

      {showBuilder && (
        <QuestionBuilder
          exams={exams} 
          initial={editingQuestion as Question} // Cast is safe because Builder handles nulls/partials gracefully usually
          onClose={() => setShowBuilder(false)}
          onCreate={handleCreate}
          onUpdate={handleUpdate}
        />
      )}
    </div>
  );
}
