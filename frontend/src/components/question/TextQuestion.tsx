import { useState } from "react";
import { autosaveAnswer } from "@/api/candidateExam";
import { Question } from "@/types/question";
interface Props {
  question: Question;
  sessionId: string;
}

export default function TextQuestion({ question, sessionId }: Props) {
  const [value, setValue] = useState("");

  const handleBlur = async () => {
    if (!value.trim()) return;

    await autosaveAnswer({
      question_id: question.id,
      answer: value,
    });
  };

  return (
    <div className="question-card">
      <p className="font-medium mb-4">{question.text}</p>

      <textarea
        className="w-full min-h-[120px]"
        value={value}
        onChange={(e) => setValue(e.target.value)}
        onBlur={handleBlur}
      />
    </div>
  );
}
