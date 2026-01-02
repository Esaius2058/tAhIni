export default function ExamRules() {
  return (
    <div className="exam-rules space-y-3 mb-8">
      <h2 className="text-lg font-semibold">Exam Instructions</h2>

      <ul className="list-disc list-inside text-sm space-y-2">
        <li>Read each question carefully before answering.</li>
        <li>You cannot pause or restart the exam once it begins.</li>
        <li>Your answers are saved automatically.</li>
        <li>Do not refresh or close the browser during the exam.</li>
        <li>The exam will be submitted automatically when time expires.</li>
      </ul>
    </div>
  );
}
