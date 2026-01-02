import { useState } from "react";
import { saveAnswer } from "@/api/candidateExam";
import { Question } from "@/types/question";

interface Props {
  question: Question;
  sessionId: string;
}

export default function MCQQuestion({ question, sessionId }: Props) {
  const [value, setValue] = useState<string | null>(null);

  const handleChange = async (optionId: string) => {
    setValue(optionId);

    await saveAnswer(sessionId, {
      question_id: question.id,
      answer: optionId,
    });
  };

  return (
    <div className="question-card">
      <p className="font-medium mb-4">{question.text}</p>

      <div className="space-y-2">
        {question.options?.map((opt) => (
          <label key={opt.id} className="flex gap-2">
            <input
              type="radio"
              name={question.id}
              checked={value === opt.id}
              onChange={() => handleChange(opt.id)}
            />
            {opt.text}
          </label>
        ))}
      </div>
    </div>
  );
}
