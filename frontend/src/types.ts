export interface DegreeSummary {
  key: string;
  name: string;
  total_credits: number;
}

export interface Course {
  code: string;
  title: string;
  credits: number;
  prereqs: string[][];
  ucc_tags: string[];
  offered: string[];
}

export interface CompletedCourse {
  code: string;
  term: string; // "PRE_COLLEGE" or "Fall 2024"
}

export interface PlanRequest {
  degree_key: string;
  completed: CompletedCourse[];
  start_term: string;
  start_year: number;
  max_credits_per_term: number;
  include_summer: boolean;
}

export interface PlannedCourse {
  code: string;
  title: string;
  credits: number;
  reason: string;
}

export interface PlannedTerm {
  term: string;
  courses: PlannedCourse[];
  credits: number;
}

export interface PlanResponse {
  degree: string;
  terms: PlannedTerm[];
  total_terms: number;
  completed_credits: number;
  remaining_credits: number;
  warnings: string[];
}