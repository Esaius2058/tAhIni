import { useEffect, useState, useRef } from "react";
import { ExamTimerProps } from "@/types/examSession";
import { AlarmClock } from "lucide-react";

export function Timer({ endsAt, onTimeUp }: ExamTimerProps) {
  const endTime = useRef(new Date(endsAt).getTime());
  const hasTriggered = useRef(false);

  const [remainingMs, setRemainingMs] = useState(
    Math.max(endTime.current - Date.now(), 0)
  );

  useEffect(() => {
    const interval = setInterval(() => {
      const diff = endTime.current - Date.now();

      if (diff <= 0) {
        setRemainingMs(0);

        if (!hasTriggered.current) {
          hasTriggered.current = true;
          onTimeUp(); // FORCE SUBMIT
        }

        clearInterval(interval);
      } else {
        setRemainingMs(diff);
      }
    }, 1000);

    return () => clearInterval(interval);
  }, [onTimeUp]);

  const minutes = Math.floor(remainingMs / 60000);
  const seconds = Math.floor((remainingMs % 60000) / 1000);

  return (
    <div className="exam-timer">
      <span className={remainingMs < 60_000 ? "text-red-600 font-bold" : ""}>
        <AlarmClock/> {minutes}:{seconds.toString().padStart(2, "0")}
      </span>
    </div>
  );
}
