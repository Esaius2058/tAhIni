// components/exam/QuestionRenderer.tsx
import MCQQuestion from "../question/MCQQuestion";
import NumericalQuestion from "../question/Numerical";
import MultiResponseQuestion from "../question/MultiResponse";
import TrueFalseQuestion from "../question/TrueFalse";
import TextQuestion from "../question/TextQuestion";
import FileUploadQuestion from "../question/FileUploadQuestion";
import { Question } from "@/types/question";

interface QuestionRendererProps {
  question: Question;
  sessionId: string;
}

export default function QuestionRenderer({
  question,
  sessionId,
}: QuestionRendererProps) {
  if (!question) return null;
  switch (question.type) {
    case "mcq":
      return <MCQQuestion question={question} sessionId={sessionId} />;

    case "multi_response":
      return (
        <MultiResponseQuestion question={question} sessionId={sessionId} />
      );

    case "true_false":
      return <TrueFalseQuestion question={question} sessionId={sessionId} />;

    case "essay":
      return <TextQuestion question={question} sessionId={sessionId} />;

    case "file_upload":
      return <FileUploadQuestion question={question} sessionId={sessionId} />;
      {
        /*<FileUploadAnswer
          sessionId={sessionId}
          questionId={question.id}
          constraints={question.constraints}
        />*/
      }

    case "short_answer":
      return <ShortAnswerQuestion question={question} sessionId={sessionId} />;

    case "numerical":
      return <NumericalQuestion question={question} sessionId={sessionId} />;

    case "code":
      return <CodeQuestion question={question} sessionId={sessionId} />;

    default:
      return <p className="text-red-600">Unsupported question type</p>;
  }
}
