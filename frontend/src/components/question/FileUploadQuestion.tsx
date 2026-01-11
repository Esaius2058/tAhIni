/*import { uploadAnswerFile } from "@/api/candidateExam";
import { Question } from "@/types/question";

interface Props {
  question: Question;
  sessionId: string;
}

export default function FileUploadQuestion({ question, sessionId }: Props) {
  const handleFileChange = async (
    e: React.ChangeEvent<HTMLInputElement>
  ) => {
    if (!e.target.files?.[0]) return;

    await uploadAnswerFile(sessionId, question.id, e.target.files[0]);
  };

  return (
    <div className="question-card">
      <p className="font-medium mb-4">{question.text}</p>

      <input type="file" onChange={handleFileChange} />
    </div>
  );
}
*/