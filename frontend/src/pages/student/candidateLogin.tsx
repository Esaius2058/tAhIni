import { useNavigate } from "react-router-dom";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { setAuthToken } from "@/lib/axios";
import { toast } from "sonner";
import { Spinner } from "@/components/ui/spinner";
import { enterExamApi, startExamApi } from "@/api/candidateExam";
import { EnterExamPayload } from "@/forms/auth/candidateLogin.types";
import { enterExamSchema } from "@/forms/auth/candidateLogin.schema";

export default function CandidateLogin() {
  const navigate = useNavigate();

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<EnterExamPayload>({
    resolver: zodResolver(enterExamSchema),
  });

  const onSubmit = async (values: EnterExamPayload) => {
    try {
      // STEP 1: Enter exam
      const enterResData = await enterExamApi(values);

      // STEP 2: Start exam
      const startRes = await startExamApi({
        examId: enterResData.exam_id, 
        candidateName: values.candidateName,
      });

      sessionStorage.setItem("examId", enterResData.exam_id);
      sessionStorage.setItem("candidateName", values.candidateName);
      localStorage.setItem("candidate_token", startRes.token);
      setAuthToken(startRes.token);
      sessionStorage.setItem("candidateExamToken", startRes.token);
      sessionStorage.setItem("sessionId", startRes.session_id);
      sessionStorage.setItem("candidateRef", startRes.candidate_ref);

      /*
      if (startRes.data.locked) {
        navigate("/student/attempt-locked");
        return;
      }*/

      navigate(`/student/instructions/${enterResData.exam_id}`);
    } catch (err: any) {
      toast.error(err.response?.data?.detail || "Unable to enter exam");
    }
  };

  return (
    <div className="form-container justify-center">
      <div>
        <img src="/tAhIni-logo.png" alt="logo" />
        <h1 className="text-xl font-bold mb-4">Exam Login</h1>
      </div>
      <form onSubmit={handleSubmit(onSubmit)} className="form-card space-y-4 items-center">
        <input
          id="candidate-name"
          placeholder="John Doe"
          className="w-[350px]"
          {...register("candidateName")}
        />
        {errors.candidateName && (
          <p className="text-red-600">{errors.candidateName.message}</p>
        )}

        <input
          id="exam-code"
          placeholder="CS-DSA-201"
          className="w-[350px]"
          {...register("examCode")}
        />
        {errors.examCode && (
          <p className="text-red-600">{errors.examCode.message}</p>
        )}

        <button disabled={isSubmitting} className="w-[300px]">
          {isSubmitting ? <Spinner /> : "Enter Exam"}
        </button>
      </form>
    </div>
  );
}
