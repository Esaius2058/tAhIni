import { useState } from "react";
import { autosaveAnswer } from "@/api/candidateExam";

export default function NumericalQuestion({ question }: any) {
  const [value, setValue] = useState<string | "">("");

  const handleBlur = async () => {
    if (value === "") return;

    await autosaveAnswer({
      question_id: question.id,
      answer:  value,
    });
  };

  return (
    <div>
      <p>{question.text}</p>

      <input
        type="number"
        value={value}
        onChange={(e) => setValue(e.target.value)}
        onBlur={handleBlur}
      />
    </div>
  );
}
