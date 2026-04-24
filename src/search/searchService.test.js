import { describe, expect, it, vi } from "vitest";

import { createSearchService } from "./searchService.js";

describe("createSearchService", () => {
  it("searches articles and profiles from one entry point", async () => {
    const search = createSearchService({
      providers: {
        getSearchableArticles: async () => [
          { id: "a-1", slug: "search-api", title: "Search API", body: "Unified search service." }
        ],
        getSearchableProfiles: async () => [
          { id: "u-1", username: "searchlead", displayName: "Search Lead", bio: "Builds search." }
        ]
      }
    });

    const response = await search("search");

    expect(response.ok).toBe(true);
    expect(response.state).toBe("results");
    expect(response.results.map((result) => result.type)).toEqual(["article", "profile"]);
    expect(response.articles).toHaveLength(1);
    expect(response.profiles).toHaveLength(1);
  });

  it("returns typed article and profile results", async () => {
    const search = createSearchService({
      providers: {
        getSearchableArticles: async () => [
          { id: "a-1", slug: "typed", title: "Typed Result", body: "Article result." }
        ],
        getSearchableProfiles: async () => [
          { id: "u-1", username: "typeduser", displayName: "Typed User", bio: "Profile result." }
        ]
      }
    });

    const response = await search("typed");

    expect(response.results).toEqual([
      expect.objectContaining({ type: "article", url: "/articles/typed" }),
      expect.objectContaining({ type: "profile", url: "/profiles/typeduser" })
    ]);
  });

  it("returns no-results state for unmatched query", async () => {
    const search = createSearchService({
      providers: {
        getSearchableArticles: async () => [{ id: "a-1", title: "One", body: "Two" }],
        getSearchableProfiles: async () => [{ id: "u-1", username: "three", displayName: "Four", bio: "Five" }]
      }
    });

    await expect(search("missing")).resolves.toMatchObject({
      ok: true,
      state: "no-results",
      results: [],
      articles: [],
      profiles: []
    });
  });

  it("does not call providers for blank queries", async () => {
    const providers = {
      getSearchableArticles: vi.fn(),
      getSearchableProfiles: vi.fn()
    };
    const search = createSearchService({ providers });

    const response = await search("   ");

    expect(response).toMatchObject({
      ok: false,
      state: "invalid-query",
      results: [],
      articles: [],
      profiles: []
    });
    expect(providers.getSearchableArticles).not.toHaveBeenCalled();
    expect(providers.getSearchableProfiles).not.toHaveBeenCalled();
  });
});
