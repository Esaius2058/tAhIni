import App from "./App";
import Landing from "./pages/Landing";
import { ProtectedRoute } from "./components/ProtectedRoute";
import Layout from "./components/Layout";
import CandidateLogin from "./pages/student/candidateLogin";
import InstructorDashboardPage from "./pages/instructor/dashboard";
import InstructorExamListPage from "./pages/instructor/exams";
import NewExamPage from "./pages/instructor/new-exam";
import SingleExamPage from "./pages/instructor/exam-details";
import InstructorQuestionsPage from "./pages/instructor/questions";
import ExamInstructionsPage from "./pages/student/instructions";
import TakeExamPage from "./pages/student/takeExam";
import SubmitExamPage from "./pages/student/submitExam";
import ExamCompletedPage from "./pages/student/completeExam";
import LockedAttempt from "./pages/student/lockedAttempt";

const MainRoutes = () => {
  const routes = [
    {
      path: "/",
      element: <App />,
      children: [
        {
          index: true,
          element: <Landing />,
        },
        {
          path: "login",
          element: <Landing />,
        },
        {
          path: "signup",
          element: <Landing />,
        },
        {
          element: <ProtectedRoute />,
          children: [
            {
              path: "instructor",
              element: <Layout />,
              children: [
                {
                  path: "dashboard",
                  element: <InstructorDashboardPage />,
                },
                {
                  path: "exams",
                  element: <InstructorExamListPage />,
                },
                {
                  path: "exams/new",
                  element: <NewExamPage />,
                },
                {
                  path: "exams/:id",
                  element: <SingleExamPage />,
                },
                {
                  path: "exams/:examId/questions",
                  element: <InstructorQuestionsPage />,
                },
              ],
            },
            {
              path: "exams/:examId",
              children: [
                // ENTRY POINTS
                {
                  //path: "/start" => to be used for links
                  path: "start",
                  element: <CandidateLogin />, // name + examCode
                },
                {
                  path: "start/student",
                  element: (
                    <ProtectedRoute>
                      <StudentExamEntry /> // no name, user already known
                    </ProtectedRoute>
                  ),
                },
                // SHARED FLOW
                {
                  path: "instructions",
                  element: <ExamInstructionsPage />,
                },
                {
                  path: "session/:sessionId",
                  element: <TakeExamPage />,
                },
                {
                  path: "submit",
                  element: <SubmitExamPage />,
                },
                {
                  path: "completed",
                  element: <ExamCompletedPage />,
                },
                {
                  path: "locked",
                  element: <LockedAttempt />,
                }
              ],
            },
          ],
        },
      ],
    },
  ];

  return routes;
};

export default MainRoutes;
