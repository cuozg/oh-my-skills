import { describe, expect, it } from "vitest";

import { validateSearchQuery } from "./validateSearchQuery.js";

describe("validateSearchQuery", () => {
  it("rejects empty and whitespace-only queries", () => {
    expect(validateSearchQuery("")).toEqual({
      ok: false,
      error: "Search query must contain at least one non-whitespace character.",
      query: "",
      terms: []
    });

    expect(validateSearchQuery(" \n\t ")).toEqual({
      ok: false,
      error: "Search query must contain at least one non-whitespace character.",
      query: "",
      terms: []
    });
  });

  it("normalizes full-text terms from a query", () => {
    expect(validateSearchQuery("  Async JavaScript, testing!  ")).toEqual({
      ok: true,
      query: "Async JavaScript, testing!",
      terms: ["async", "javascript", "testing"]
    });
  });
});
