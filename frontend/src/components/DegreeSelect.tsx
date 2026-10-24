import type { DegreeSummary } from "../types";

interface Props {
  degrees: DegreeSummary[];
  value: string;
  onChange: (key: string) => void;
}

export default function DegreeSelect({ degrees, value, onChange }: Props) {
  return (
    <div className="card">
      <h2>1. Choose your degree</h2>
      <select value={value} onChange={(e) => onChange(e.target.value)}>
        <option value="">— Select a degree —</option>
        {degrees.map((d) => (
          <option key={d.key} value={d.key}>
            {d.name} ({d.total_credits} cr)
          </option>
        ))}
      </select>
    </div>
  );
}