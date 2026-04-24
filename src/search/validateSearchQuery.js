import { SEARCH_QUERY_ERROR } from "./searchTypes.js";
import { tokenize } from "./fullText.js";

export function validateSearchQuery(query) {
  const normalizedQuery = String(query ?? "").trim();

  if (normalizedQuery.length === 0) {
    return {
      ok: false,
      error: SEARCH_QUERY_ERROR,
      query: "",
      terms: []
    };
  }

  return {
    ok: true,
    query: normalizedQuery,
    terms: tokenize(normalizedQuery)
  };
}
