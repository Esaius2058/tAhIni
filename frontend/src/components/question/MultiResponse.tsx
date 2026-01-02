import { autosaveAnswer } from "@/api/candidateExam";
import { useState } from "react";

export default function MultiResponseQuestion({ question, sessionId }: any) {
  const [selected, setSelected] = useState<string[]>([]);

  const toggle = async (id: string) => {
    const next = selected.includes(id)
      ? selected.filter((x) => x !== id)
      : [...selected, id];

    setSelected(next);

    await autosaveAnswer({
      question_id: question.id,
      answer: next,
    });
  };

  return (
    <div>
      <p>{question.text}</p>

      {question.options?.map((opt: any) => (
        <label key={opt.id}>
          <input
            type="checkbox"
            checked={selected.includes(opt.id)}
            onChange={() => toggle(opt.id)}
          />
          {opt.text}
        </label>
      ))}
    </div>
  );
}
