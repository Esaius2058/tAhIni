import { autosaveAnswer } from "@/api/candidateExam";

export default function TrueFalseQuestion({ question, sessionId }: any) {
  const handleChange = async (value: boolean) => {
    await autosaveAnswer({
      question_id: question.id,
      answer: String(value),
    });
  };

  return (
    <div>
      <p>{question.text}</p>

      <label>
        <input type="radio" onChange={() => handleChange(true)} />
        True
      </label>

      <label>
        <input type="radio" onChange={() => handleChange(false)} />
        False
      </label>
    </div>
  );
}
