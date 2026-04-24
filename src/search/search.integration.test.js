import { describe, expect, it } from "vitest";

import { searchFixtures } from "./__fixtures__/searchFixtures.js";
import { createInMemorySearchProviders } from "./searchProviders.js";
import { createSearchService } from "./searchService.js";

describe("search integration", () => {
  it("search consumes visible fixtures without changing browsing or discovery data", async () => {
    const fixturesBefore = structuredClone(searchFixtures);
    const search = createSearchService({
      providers: createInMemorySearchProviders(searchFixtures)
    });

    const response = await search("full text search");

    expect(response.ok).toBe(true);
    expect(response.results.map((result) => result.type)).toEqual(["article", "profile"]);
    expect(response.articles.every((result) => result.type === "article")).toBe(true);
    expect(response.profiles.every((result) => result.type === "profile")).toBe(true);
    expect(response.results.find((result) => result.id === "article-draft")).toBeUndefined();
    expect(response.results.find((result) => result.id === "profile-private")).toBeUndefined();
    expect(searchFixtures).toEqual(fixturesBefore);
  });
});
