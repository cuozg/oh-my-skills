import { searchArticles } from "./articleSearch.js";
import { searchProfiles } from "./profileSearch.js";
import { SEARCH_STATES } from "./searchTypes.js";
import { validateSearchQuery } from "./validateSearchQuery.js";

export function createSearchService({ providers }) {
  assertProviders(providers);

  return async function search(query) {
    const validation = validateSearchQuery(query);

    if (!validation.ok) {
      return createSearchResponse({
        ok: false,
        state: SEARCH_STATES.INVALID_QUERY,
        query: validation.query,
        error: validation.error,
        articles: [],
        profiles: []
      });
    }

    const [articleRecords, profileRecords] = await Promise.all([
      providers.getSearchableArticles({ query: validation.query, terms: validation.terms }),
      providers.getSearchableProfiles({ query: validation.query, terms: validation.terms })
    ]);

    const articles = searchArticles({ query: validation.query, articles: articleRecords });
    const profiles = searchProfiles({ query: validation.query, profiles: profileRecords });

    return createSearchResponse({
      ok: true,
      state: articles.length + profiles.length > 0 ? SEARCH_STATES.RESULTS : SEARCH_STATES.NO_RESULTS,
      query: validation.query,
      articles,
      profiles
    });
  };
}

function assertProviders(providers) {
  if (
    providers == null ||
    typeof providers.getSearchableArticles !== "function" ||
    typeof providers.getSearchableProfiles !== "function"
  ) {
    throw new TypeError("Search providers must include getSearchableArticles and getSearchableProfiles functions.");
  }
}

function createSearchResponse({ ok, state, query, error, articles, profiles }) {
  const combinedResults = [...articles, ...profiles];

  return {
    ok,
    state,
    query,
    error,
    results: combinedResults,
    articles: [...articles],
    profiles: [...profiles],
    meta: {
      total: combinedResults.length,
      articles: articles.length,
      profiles: profiles.length
    }
  };
}
