import { useEffect, useState } from "react";
import { Question } from "@/types/question";
import { autosaveAnswer } from "@/api/candidateExam";

type Props = {
  question: Question;
  sessionId: string;
};

export function CodeQuestion({ question }: Props) {
  const [code, setCode] = useState("");
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    if (!code) return;

    const timeout = setTimeout(async () => {
      try {
        setSaving(true);
        await autosaveAnswer({ question_id: question.id, answer: code,});
      } finally {
        setSaving(false);
      }
    }, 1000);

    return () => clearTimeout(timeout);
  }, [code, question.id]);

  return (
    <div className="space-y-2">
      <p className="font-medium">{question.text}</p>

      <textarea
        className="w-full min-h-[220px] font-mono rounded border p-2"
        placeholder={`Write your code here…`}
        value={code}
        onChange={(e) => setCode(e.target.value)}
      />
    </div>
  );
}
