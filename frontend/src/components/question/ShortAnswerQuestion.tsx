import { useEffect, useState } from "react";
import { Question } from "@/types/question";
import { autosaveAnswer } from "@/api/candidateExam";
import { Spinner } from "../ui/spinner";

type Props = {
  question: Question;
  sessionId: string; 
};

export function ShortAnswerQuestion({ question }: Props) {
  const [answer, setAnswer] = useState("");
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    if (!answer) return;

    const timeout = setTimeout(async () => {
      try {
        setSaving(true);
        await autosaveAnswer({
          question_id: question.id,
          answer,
        });
      } finally {
        setSaving(false);
      }
    }, 1000); // every 2 seconds

    return () => clearTimeout(timeout);
  }, [answer, question.id]);

  return (
    <div className="space-y-2">
      <p className="font-medium">{question.text}</p>

      <textarea
        className="w-full min-h-[120px] rounded border p-2"
        placeholder="Type your answer here..."
        value={answer}
        onChange={(e) => setAnswer(e.target.value)}
      />

      <span className="text-xs text-muted-foreground">
        {saving ? <Spinner/> : "Saved"}
      </span>
    </div>
  );
}
