import { useState } from "react";
import { Question, Answer, QuestionType } from "../../types/question";

interface QuestionBuilderProps {
  initial?: Question | null;
  onClose: () => void;
  onCreate: (question: Question) => void;
  onUpdate: (question: Question) => void;
}

export default function QuestionBuilder({
  initial,
  onClose,
  onCreate,
  onUpdate,
}: QuestionBuilderProps) {
  const [text, setText] = useState(initial?.text || "");
  const [type, setType] = useState<QuestionType>(initial?.type || "mcq");
  const [answers, setAnswers] = useState<Answer[]>(
    initial?.answers || [
      { id: crypto.randomUUID(), text: "", is_correct: true },
    ]
  );

  const updateAnswer = (index: number, key: keyof Answer, value: any) => {
    const updated = [...answers];
    updated[index] = { ...updated[index], [key]: value };
    setAnswers(updated);
  };

  const addAnswer = () => {
    setAnswers((prev) => [
      ...prev,
      { id: crypto.randomUUID(), text: "", is_correct: false },
    ]);
  };

  const handleSubmit = () => {
    const payload: Question = {
      id: initial?.id || crypto.randomUUID(),
      text,
      type,
      difficulty: initial?.difficulty || "medium",
      tags: initial?.tags || [],
      answers,
    };

    initial ? onUpdate(payload) : onCreate(payload);
    onClose();
  };

  return (
    <div className="p-4 space-y-4">
      <h2 className="text-lg font-bold">
        {initial ? "Edit Question" : "Create Question"}
      </h2>
      <input
        className="w-full border p-2"
        value={text}
        placeholder="Question text"
        onChange={(e) => setText(e.target.value)}
      />

      {/* Question type */}
      <select
        className="w-full border p-2"
        value={type}
        onChange={(e) => setType(e.target.value as QuestionType)}
      >
        <option value="mcq">MCQ</option>
        <option value="multi_response">Multi-Response</option>
        <option value="true_false">True/False</option>
        <option value="short_answer">Short Answer</option>
        <option value="essay">Essay</option>
        <option value="code">Code</option>
        <option value="numerical">Numerical</option>
      </select>

      {/* Answers */}
      <div className="space-y-2">
        {answers.map((a, i) => (
          <div key={a.id} className="flex items-center gap-2">
            <input
              className="flex-1 border p-2"
              value={a.text}
              placeholder={`Answer ${i + 1}`}
              onChange={(e) => updateAnswer(i, "text", e.target.value)}
            />

            <input
              type="checkbox"
              checked={a.is_correct}
              onChange={(e) => updateAnswer(i, "is_correct", e.target.checked)}
            />
            <span>Correct</span>
          </div>
        ))}

        <button onClick={addAnswer} className="px-3 py-1 bg-gray-500 rounded hover:scale-110">
          Add Answer
        </button>
      </div>

      {/* Action buttons */}
      <div className="flex w-full justify-center gap-3">
        <button className="px-3 py-1 bg-blue-600 hover:bg-blue-800 hover:scale-110" onClick={handleSubmit}>
          {initial ? "Update" : "Create"}
        </button>

        <button className="px-3 py-1 hover:scale-110" onClick={onClose}>
          Cancel
        </button>
      </div>
    </div>
  );
}
