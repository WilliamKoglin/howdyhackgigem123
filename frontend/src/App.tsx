import { useEffect, useMemo, useState } from "react";
import type {
  Course,
  CompletedCourse,
  DegreeSummary,
  PlanResponse,
} from "./types";
import { fetchCourses, fetchDegrees, generatePlan } from "./api";
import DegreeSelect from "./components/DegreeSelect";
import CreditEntry from "./components/CreditEntry";
import PlanView from "./components/PlanView";

export default function App() {
  const [degrees, setDegrees] = useState<DegreeSummary[]>([]);
  const [courses, setCourses] = useState<Course[]>([]);
  const [degreeKey, setDegreeKey] = useState("");
  const [completed, setCompleted] = useState<CompletedCourse[]>([]);

  const [startTerm, setStartTerm] = useState("Fall");
  const [startYear, setStartYear] = useState(new Date().getFullYear());
  const [maxCredits, setMaxCredits] = useState(15);
  const [includeSummer, setIncludeSummer] = useState(false);

  const [plan, setPlan] = useState<PlanResponse | null>(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  // Load catalog + degrees once on mount.
  useEffect(() => {
    Promise.all([fetchDegrees(), fetchCourses()])
      .then(([d, c]) => {
        setDegrees(d);
        setCourses(c);
      })
      .catch((e) => setError(e.message));
  }, []);

  // Build a list of past term labels for the "completed in which semester" dropdown.
  const pastTerms = useMemo(() => {
    const labels: string[] = [];
    const seasons = ["Spring", "Summer", "Fall"];
    const nowYear = new Date().getFullYear();
    for (let y = nowYear - 4; y <= nowYear; y++) {
      for (const s of seasons) labels.push(`${s} ${y}`);
    }
    return labels.reverse();
  }, []);

  async function handleGenerate() {
    setError("");
    setLoading(true);
    setPlan(null);
    try {
      const result = await generatePlan({
        degree_key: degreeKey,
        completed,
        start_term: startTerm,
        start_year: startYear,
        max_credits_per_term: maxCredits,
        include_summer: includeSummer,
      });
      setPlan(result);
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="app">
      <header>
        <h1>🎓 Texas A&amp;M Degree Planner</h1>
        <p>Plan your path to graduation, semester by semester.</p>
      </header>

      {error && <div className="error">{error}</div>}

      <DegreeSelect degrees={degrees} value={degreeKey} onChange={setDegreeKey} />

      <CreditEntry
        courses={courses}
        completed={completed}
        onChange={setCompleted}
        terms={pastTerms}
      />

      <div className="card">
        <h2>3. Planning options</h2>
        <div className="options">
          <label>
            Next term starts
            <select value={startTerm} onChange={(e) => setStartTerm(e.target.value)}>
              <option value="Fall">Fall</option>
              <option value="Spring">Spring</option>
              <option value="Summer">Summer</option>
            </select>
          </label>
          <label>
            Year
            <input
              type="number"
              value={startYear}
              onChange={(e) => setStartYear(Number(e.target.value))}
            />
          </label>
          <label>
            Max credits / term
            <input
              type="number"
              min={3}
              max={21}
              value={maxCredits}
              onChange={(e) => setMaxCredits(Number(e.target.value))}
            />
          </label>
          <label className="checkbox">
            <input
              type="checkbox"
              checked={includeSummer}
              onChange={(e) => setIncludeSummer(e.target.checked)}
            />
            Include summer terms
          </label>
        </div>

        <button
          className="generate"
          disabled={!degreeKey || loading}
          onClick={handleGenerate}
        >
          {loading ? "Planning…" : "Generate my plan"}
        </button>
      </div>

      {plan && <PlanView plan={plan} />}
    </div>
  );
}