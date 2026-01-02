interface ExamHeaderProps {
  exam: {
    title: string;
    duration_minutes: number;
  } | null;
}

export default function ExamHeader({ exam }: ExamHeaderProps) {
  if (!exam) return null;

  return (
    <div className="exam-header mb-6">
      <h1 className="text-2xl font-bold">{exam.title}</h1>

      <p className="text-sm text-muted-foreground mt-1">
        Duration: {exam.duration_minutes} minutes
      </p>
    </div>
  );
}
