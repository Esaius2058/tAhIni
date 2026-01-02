"use client";
import { Link } from "react-router-dom";

export default function InstructorDashboardPage() {
  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Instructor Dashboard</h1>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <Link
          to="/instructor/exams"
          className="p-6 border rounded-lg hover:bg-gray-50 transition"
        >
          <h2 className="font-semibold text-xl mb-2">Manage Exams</h2>
          <p className="text-gray-600">
            View, edit, and create exams for your students.
          </p>
        </Link>

        <Link
          to="/instructor/exams/new"
          className="p-6 border rounded-lg hover:bg-gray-50 transition"
        >
          <h2 className="font-semibold text-xl mb-2">Create New Exam</h2>
          <p className="text-gray-600">
            Build a fresh exam from scratch.
          </p>
        </Link>
      </div>
    </div>
  );
}
