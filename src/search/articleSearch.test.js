import { describe, expect, it } from "vitest";

import { searchArticles } from "./articleSearch.js";

describe("searchArticles", () => {
  it("matches article title and body using full-text terms", () => {
    const results = searchArticles({
      query: "async testing",
      articles: [
        {
          id: "a-1",
          slug: "async-testing",
          title: "Async Testing Patterns",
          body: "Use integration tests for promise-heavy workflows."
        },
        {
          id: "a-2",
          slug: "unrelated",
          title: "Editor Setup",
          body: "Configure fonts and themes."
        }
      ]
    });

    expect(results).toHaveLength(1);
    expect(results[0]).toMatchObject({
      id: "a-1",
      type: "article",
      title: "Async Testing Patterns",
      slug: "async-testing",
      matchedFields: ["title", "body"]
    });
  });

  it("ranks article matches by relevance", () => {
    const results = searchArticles({
      query: "search ranking",
      articles: [
        {
          id: "a-low",
          slug: "body-only",
          title: "Implementation Notes",
          body: "Search appears once in this body."
        },
        {
          id: "a-high",
          slug: "search-ranking",
          title: "Search Ranking Search",
          body: "Ranking signals and search relevance are covered here."
        }
      ]
    });

    expect(results.map((result) => result.id)).toEqual(["a-high", "a-low"]);
    expect(results[0].score).toBeGreaterThan(results[1].score);
  });

  it("does not mutate source article records", () => {
    const articles = [
      {
        id: "a-1",
        slug: "immutable",
        title: "Immutable Search",
        body: "Search copies source records."
      }
    ];

    const before = structuredClone(articles);
    searchArticles({ query: "search", articles });

    expect(articles).toEqual(before);
  });
});
