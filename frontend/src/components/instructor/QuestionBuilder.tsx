import { useState, useEffect } from "react";
import { Question, Answer, QuestionType } from "../../types/question";
import { ExamRead } from "@/types/exam";
import { toast } from "sonner";
import { Spinner } from "../ui/spinner";

interface QuestionBuilderProps {
  initial?: Question | null; 
  exams: ExamRead[]; 
  onClose: () => void;
  onCreate: (question: Question) => Promise<void> | void;
  onUpdate: (question: Question) => Promise<void> | void;
}

export default function QuestionBuilder({
  initial,
  exams,
  onClose,
  onCreate,
  onUpdate,
}: QuestionBuilderProps) {
  const [text, setText] = useState(initial?.text || "");
  const [type, setType] = useState<QuestionType>(initial?.type || "mcq");
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Determine if we are "Editing" based on whether a DB ID exists
  const isEditMode = !!initial?.id;

  const [selectedExamId, setSelectedExamId] = useState<string>(
    initial?.exam_id || (exams.length > 0 ? exams[0].id : "")
  );

  // Initialize options state.
  // We check 'initial?.answer?.options' because of the new nested architecture.
  const [answers, setAnswers] = useState<Answer[]>(
    initial?.answer?.options || [
      { id: crypto.randomUUID(), text: "", is_correct: false },
    ]
  );

  // Safety check: Select first exam if none selected
  useEffect(() => {
    if (!selectedExamId && exams.length > 0) {
      setSelectedExamId(exams[0].id);
    }
  }, [exams, selectedExamId]);

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

  const removeAnswer = (index: number) => {
    setAnswers((prev) => prev.filter((_, i) => i !== index));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault(); 

    if (!text) return toast.error("Question text is required");
    if (!selectedExamId) return toast.error("Please select an exam");

    setIsSubmitting(true);
    // Construct the payload with the nested 'answer' container
    const payload: Question = {
      id: initial?.id || crypto.randomUUID(),
      text,
      type,
      exam_id: selectedExamId, 
      difficulty: initial?.difficulty || "medium",
      tags: initial?.tags || [],
      answer: {
        id: initial?.answer?.id || crypto.randomUUID(), 
        options: answers 
      },
    };

    try {
      if (isEditMode) {
        await onUpdate(payload);
      } else {
        await onCreate(payload);
      }
      toast.success("Question added successfully");
      onClose();
    } catch (error) {
      console.error("Error saving question:", error);
    } finally{
      setIsSubmitting(false);
    }
  };

  return (
    <div className="p-4 space-y-4 question-form-container bg-white rounded-lg shadow-sm">
      <form onSubmit={handleSubmit} className="form-card space-y-4">
        <h2 className="text-lg font-bold">
          {isEditMode ? "Edit Question" : "Create Question"}
        </h2>

        {/* Exam Selection */}
        <div className="flex flex-col gap-1">
          <label className="text-sm font-medium text-gray-700">Assign to Exam</label>
          <select 
            className="w-full border p-2 rounded bg-white"
            value={selectedExamId}
            onChange={(e) => setSelectedExamId(e.target.value)}
          >
            <option value="" disabled>Select an Exam</option>
            {exams.map((exam) => (
              <option key={exam.id} value={exam.id}>
                {exam.title || "Untitled Exam"}
              </option>
            ))}
          </select>
        </div>

        {/* Question Text */}
        <div className="flex flex-col gap-1">
            <label className="text-sm font-medium text-gray-700">Question Text</label>
            <textarea
              className="w-full bg-white border p-2 rounded min-h-[80px]"
              value={text}
              placeholder="Enter your question here..."
              onChange={(e) => setText(e.target.value)}
            />
        </div>

        {/* Question type */}
        <div className="flex flex-col gap-1">
            <label className="text-sm font-medium text-gray-700">Question Type</label>
            <select
              className="w-full border p-2 rounded bg-white"
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
        </div>

        {/* Answers - Only show for choice-based questions */}
        {(type === "mcq" || type === "true_false" || type === "multi_response") && (
          <div className="space-y-3 pt-3">
            <label className="text-sm font-medium text-gray-700">Answer Options</label>
            
            {answers.map((a, i) => (
              <div key={a.id} className="flex items-center gap-2">
                {/* Input Field */}
                <input
                  className="flex-1 p-2 border rounded"
                  value={a.text}
                  placeholder={`Option ${i + 1}`}
                  onChange={(e) => updateAnswer(i, "text", e.target.value)}
                />

                {/* Correct Checkbox */}
                <div className="flex items-center gap-2 px-2">
                    <input
                      type="checkbox"
                      id={`correct-${a.id}`}
                      checked={a.is_correct}
                      className="w-4 h-4 cursor-pointer"
                      onChange={(e) => updateAnswer(i, "is_correct", e.target.checked)}
                    />
                    <label htmlFor={`correct-${a.id}`} className="text-sm cursor-pointer select-none">
                      Correct
                    </label>
                </div>

                {/* Remove Button */}
                {answers.length > 1 && (
                  <button
                    type="button"
                    onClick={() => removeAnswer(i)}
                    className="bg-transparent text-black rounded-full"
                    title="Remove option"
                  >
                    ✕
                  </button>
                )}
              </div>
            ))}

            <button
              type="button" 
              onClick={addAnswer}
              className="px-3 py-1 text-sm bg-gray-100 border border-gray-300 rounded hover:bg-gray-200 hover:text-black transition text-gray-700"
            >
              + Add Option
            </button>
          </div>
        )}

        {/* Action buttons */}
        <div className="flex w-full justify-end gap-3 pt-4">
          <button 
            type="button" 
            className="" 
            onClick={onClose}
          >
            Cancel
          </button>
          
          <button 
            type="submit" 
            disabled={isSubmitting}
            className="bg-blue-600 text-white hover:bg-blue-700 transition flex items-center gap-2 disabled:opacity-70 disabled:cursor-not-allowed min-w-[140px]"
          >
            {isSubmitting ? (
              <>
                <Spinner />
                {isEditMode ? "Updating..." : "Saving..."}
              </>
            ) : (
              isEditMode ? "Update Question" : "Add Question"
            )}
          </button>
        </div>
      </form>
    </div>
  );
}