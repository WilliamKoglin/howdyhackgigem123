import type { PlanResponse } from "../types";

export default function PlanView({ plan }: { plan: PlanResponse }) {
  return (
    <div className="card plan">
      <h2>Recommended plan — {plan.degree}</h2>
      <div className="summary">
        <span>✅ {plan.completed_credits} cr completed</span>
        <span>📚 {plan.remaining_credits} cr remaining</span>
        <span>🎓 {plan.total_terms} term(s) to graduate</span>
      </div>

      {plan.warnings.length > 0 && (
        <ul className="warnings">
          {plan.warnings.map((w, i) => (
            <li key={i}>⚠️ {w}</li>
          ))}
        </ul>
      )}

      <div className="terms">
        {plan.terms.map((term) => (
          <div key={term.term} className="term-card">
            <h3>
              {term.term} <span className="cr">({term.credits} cr)</span>
            </h3>
            <ul>
              {term.courses.map((c) => (
                <li key={c.code}>
                  <strong>{c.code}</strong> — {c.title}{" "}
                  <span className="cr">({c.credits})</span>
                  <div className="reason">{c.reason}</div>
                </li>
              ))}
            </ul>
          </div>
        ))}
      </div>
    </div>
  );
}