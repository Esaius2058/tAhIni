import { useNavigate } from "react-router-dom";
import { Header } from "@/components/Header";

export default function Landing() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-background text-foreground flex flex-col">
      <Header />

      <main className="flex-1">
        {/* HERO */}
        <section className="max-w-6xl mx-auto px-6 py-24 text-center">
          <h1 className="text-4xl md:text-5xl font-bold tracking-tight mb-6">
            Secure. Fair. Distraction-Free.
            <br />
            <span className="text-primary">Exams, done right.</span>
          </h1>

          <p className="text-muted-foreground max-w-2xl mx-auto mb-10">
            tAhIni is a secure digital examination platform designed to eliminate
            malpractice, reduce administrative overhead, and deliver a seamless
            exam experience for both candidates and institutions.
          </p>

          <div className="flex flex-col sm:flex-row justify-center gap-4">
            <button
              onClick={() => navigate("/exams/enter")}
            >
              Enter an Exam
            </button>

            <button
              onClick={() => navigate("/login")}
            >
              Instructor Login
            </button>
          </div>
        </section>

        {/* FEATURES */}
        <section className="bg-muted/40 py-20">
          <div className="max-w-6xl mx-auto px-6 grid md:grid-cols-3 gap-10">
            <Feature
              title="Secure Exam Sessions"
              description="Token-based exam sessions ensure each attempt is authenticated, isolated, and tamper-proof."
            />

            <Feature
              title="Autosave by Default"
              description="Every answer is saved in real-time. Power outage? Network glitch? Student panic? Covered."
            />

            <Feature
              title="Built for Scale"
              description="Supports guest candidates and registered students with a unified session model."
            />
          </div>
        </section>

        {/* HOW IT WORKS */}
        <section className="max-w-6xl mx-auto px-6 py-20">
          <h2 className="text-2xl font-semibold text-center mb-12">
            How tAhIni Works
          </h2>

          <div className="grid md:grid-cols-3 gap-10 text-center">
            <Step
              number="1"
              title="Create Exam"
              description="Instructors design exams with multiple question types and strict timing rules."
            />
            <Step
              number="2"
              title="Candidate Entry"
              description="Candidates enter via exam code or institutional login — no unnecessary friction."
            />
            <Step
              number="3"
              title="Secure Submission"
              description="Once submitted, attempts are locked and ready for grading."
            />
          </div>
        </section>
      </main>

      {/* FOOTER */}
      <footer className="bg-[#f5f5f5] py-8 text-center text-sm text-muted-foreground">
        © {new Date().getFullYear()} tAhIni. Built for academic integrity.
      </footer>
    </div>
  );
}

/* -------------------------------------------------------------------------- */

function Feature({
  title,
  description,
}: {
  title: string;
  description: string;
}) {
  return (
    <div className="p-6 bg-background rounded-lg border shadow-sm">
      <h3 className="font-semibold mb-2">{title}</h3>
      <p className="text-sm text-muted-foreground">{description}</p>
    </div>
  );
}

function Step({
  number,
  title,
  description,
}: {
  number: string;
  title: string;
  description: string;
}) {
  return (
    <div className="flex flex-col items-center">
      <div className="w-12 h-12 mb-4 rounded-full bg-primary/10 text-primary flex items-center justify-center font-bold text-lg">
        {number}
      </div>
      <h3 className="font-medium mb-2">{title}</h3>
      <p className="text-sm text-muted-foreground max-w-xs">{description}</p>
    </div>
  );
}