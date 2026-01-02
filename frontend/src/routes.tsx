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
          //path: "exams/:examId/entry" => to be used for links
          path: "exams/candidate/entry", //for testing
          element: <CandidateLogin />
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
          ],
        },
      ],
    },
  ];

  return routes;
};

export default MainRoutes;
