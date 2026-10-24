import type { Course, CompletedCourse } from "../types";

interface Props {
  courses: Course[];
  completed: CompletedCourse[];
  onChange: (completed: CompletedCourse[]) => void;
  terms: string[]; // available term labels
}

export default function CreditEntry({ courses, completed, onChange, terms }: Props) {
  const completedMap = new Map(completed.map((c) => [c.code, c.term]));

  function toggle(code: string, checked: boolean) {
    if (checked) {
      onChange([...completed, { code, term: "PRE_COLLEGE" }]);
    } else {
      onChange(completed.filter((c) => c.code !== code));
    }
  }

  function setTerm(code: string, term: string) {
    onChange(completed.map((c) => (c.code === code ? { ...c, term } : c)));
  }

  return (
    <div className="card">
      <h2>2. Mark completed credits</h2>
      <p className="hint">
        Check any course you've finished and set the term. Use{" "}
        <strong>Before college</strong> for AP, dual-credit, or transfer work.
      </p>
      <div className="course-grid">
        {courses.map((c) => {
          const isDone = completedMap.has(c.code);
          return (
            <div key={c.code} className={`course-row ${isDone ? "done" : ""}`}>
              <label>
                <input
                  type="checkbox"
                  checked={isDone}
                  onChange={(e) => toggle(c.code, e.target.checked)}
                />
                <span className="code">{c.code}</span>
                <span className="title">{c.title}</span>
                <span className="cr">{c.credits} cr</span>
              </label>
              {isDone && (
                <select
                  value={completedMap.get(c.code)}
                  onChange={(e) => setTerm(c.code, e.target.value)}
                >
                  <option value="PRE_COLLEGE">Before college</option>
                  {terms.map((t) => (
                    <option key={t} value={t}>
                      {t}
                    </option>
                  ))}
                </select>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}