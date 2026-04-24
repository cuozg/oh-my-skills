import { describe, expect, it } from "vitest";

import { searchProfiles } from "./profileSearch.js";

describe("searchProfiles", () => {
  it("matches display name username and bio using full-text terms", () => {
    const results = searchProfiles({
      query: "design mentor",
      profiles: [
        {
          id: "u-1",
          username: "designmentor",
          displayName: "Mina Design",
          bio: "Mentor for product teams and design systems."
        },
        {
          id: "u-2",
          username: "backendalex",
          displayName: "Alex Backend",
          bio: "Works on queues."
        }
      ]
    });

    expect(results).toHaveLength(1);
    expect(results[0]).toMatchObject({
      id: "u-1",
      type: "profile",
      username: "designmentor",
      displayName: "Mina Design",
      matchedFields: ["displayName", "username", "bio"]
    });
  });

  it("ranks profile matches by relevance", () => {
    const results = searchProfiles({
      query: "search expert",
      profiles: [
        {
          id: "u-low",
          username: "finder",
          displayName: "Jordan Finder",
          bio: "Search support."
        },
        {
          id: "u-high",
          username: "search-expert",
          displayName: "Search Expert",
          bio: "Search expert for relevance tuning."
        }
      ]
    });

    expect(results.map((result) => result.id)).toEqual(["u-high", "u-low"]);
    expect(results[0].score).toBeGreaterThan(results[1].score);
  });
});
