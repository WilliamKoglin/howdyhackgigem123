import type { Course, DegreeSummary, PlanRequest, PlanResponse } from "./types";

const BASE = "http://localhost:8000";

export async function fetchDegrees(): Promise<DegreeSummary[]> {
  const res = await fetch(`${BASE}/degrees`);
  if (!res.ok) throw new Error("Failed to load degrees");
  return res.json();
}

export async function fetchCourses(): Promise<Course[]> {
  const res = await fetch(`${BASE}/courses`);
  if (!res.ok) throw new Error("Failed to load courses");
  return res.json();
}

export async function generatePlan(req: PlanRequest): Promise<PlanResponse> {
  const res = await fetch(`${BASE}/plan`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(req),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail ?? "Failed to generate plan");
  }
  return res.json();
}