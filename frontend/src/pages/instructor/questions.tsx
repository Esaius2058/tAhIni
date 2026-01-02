import { useEffect, useState } from "react";
import { Plus, Pencil, Trash } from "lucide-react";
import { Question } from "../../types/question";
import QuestionBuilder from "../../components/instructor/QuestionBuilder";
import { useParams } from "react-router-dom";

export default function InstructorQuestionsPage() {
  const { id: examId } = useParams(); 
  const [loading, setLoading] = useState(true);
  const [questions, setQuestions] = useState<Question[]>([]);
  const [showBuilder, setShowBuilder] = useState(false);
  const [editingQuestion, setEditingQuestion] = useState<Question | null>(null);

  useEffect(() => {
    setTimeout(() => {
      setQuestions([
        {
          id: "q1",
          text: "What is the capital of France?",
          type: "mcq",
          difficulty: "easy",
          tags: [],
          answers: [
            { id: crypto.randomUUID(), text: "Paris", is_correct: true },
            { id: crypto.randomUUID(), text: "London", is_correct: false },
            { id: crypto.randomUUID(), text: "Berlin", is_correct: false },
          ],
        },
        {
          id: "q2",
          text: `An algorithm design technique is a general approach to solving problems algorithmically that
                is applicable to a variety of problems from different areas of computing. Algorithms lie at the
                heart of computing. If we observe our surroundings, we can find several algorithms working to
                solve our daily life problems. Using real world applications, discuss the following algorithms.\n
                (i) Brute force (4 Marks)\n
                (ii) Backtracking`,
          type: "essay",
          difficulty: "medium",
          tags: [],
          answers: [],
        },
      ]);
      setLoading(false);
    }, 600);
  }, [examId]);

  const handleCreate = (question: Question) => {
    setQuestions((prev) => [...prev, { ...question, id: crypto.randomUUID() }]);
  };

  const handleUpdate = (updated: Question) => {
    setQuestions((prev) =>
      prev.map((q) => (q.id === updated.id ? updated : q))
    );
  };

  const handleDelete = (id: string) => {
    setQuestions((prev) => prev.filter((q) => q.id !== id));
  };

  const questionType = (type: string) => {
    if (type == "true_false"){
      return "True / False";
    }else if (type == "mcq"){
      return "MCQ"
    } else if (type == "short_answer"){
      return "Short Answer"
    } else if (type == "multi_response"){
      return "Multi Response";
    } 
    return type;
  }

  if (loading) return <div>Loading questions…</div>;

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-xl font-semibold">Questions for Exam {examId}</h1>
        <button
          className="flex gap-2 items-center px-3 py-2 rounded hover:scale-110"
          onClick={() => {
            setEditingQuestion(null);
            setShowBuilder(true);
          }}
        >
          <Plus size={18} />
        </button>
      </div>

      {/* QUESTIONS TABLE */}
      <div className="bg-white p-4 rounded">
        <table className="w-full">
          <thead>
            <tr className="text-left border-b">
              <th className="py-2">Question</th>
              <th className="py-2">Type</th>
            </tr>
          </thead>
          <tbody>
            {questions.map((q) => (
              <tr key={q.id} className="text-left border-b">
                <td className="py-2">{q.text}</td>
                <td className="capitalize">{questionType(q.type)}</td>
                <td>
                  <div className="flex gap-3">
                    <button
                      onClick={() => {
                        setEditingQuestion(q);
                        setShowBuilder(true);
                      }}
                      className="bg-transparent text-black transition duration-300 ease-in-out hover:text-black hover:bg-transparent hover:scale-110"
                    >
                      <Pencil size={18} />
                    </button>

                    <button
                      onClick={() => handleDelete(q.id)}
                      className="bg-transparent text-black transition duration-300 ease-in-out hover:text-black hover:bg-transparent hover:scale-110"
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
          <p className="text-gray-500 text-center py-6">
            No questions yet. Add one!
          </p>
        )}
      </div>

      {showBuilder && (
        <QuestionBuilder
          initial={editingQuestion}
          onClose={() => setShowBuilder(false)}
          onCreate={handleCreate}
          onUpdate={handleUpdate}
        />
      )}
    </div>
  );
}
