import { describe, expect, it } from "vitest";

import { createInMemorySearchProviders } from "./searchProviders.js";

describe("createInMemorySearchProviders", () => {
  it("uses provider boundaries without mutating source records", async () => {
    const articles = [
      { id: "a-public", title: "Public", body: "Visible.", visibility: "public", status: "published" },
      { id: "a-draft", title: "Draft", body: "Hidden.", visibility: "public", status: "draft" }
    ];
    const profiles = [
      { id: "u-public", username: "public", displayName: "Public User", bio: "Visible.", visibility: "public" },
      { id: "u-private", username: "private", displayName: "Private User", bio: "Hidden.", visibility: "private" }
    ];
    const before = structuredClone({ articles, profiles });

    const providers = createInMemorySearchProviders({ articles, profiles });

    await expect(providers.getSearchableArticles()).resolves.toEqual([articles[0]]);
    await expect(providers.getSearchableProfiles()).resolves.toEqual([profiles[0]]);
    expect({ articles, profiles }).toEqual(before);
  });
});
