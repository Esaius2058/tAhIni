export default function ExamHeader() {
  if (!sessionStorage.getItem("examId")) return null;

  return (
    <div className="exam-header mb-6">
      <h1 className="text-2xl font-bold">{sessionStorage.getItem("examTitle")}</h1>

      <p className="text-sm text-muted-foreground mt-1">
        Duration: {sessionStorage.getItem("examDuration")} minutes
      </p>
    </div>
  );
}
