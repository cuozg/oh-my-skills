import { describe, expect, it } from "vitest";

import {
  ARTICLE_RESULT_TYPE,
  PROFILE_RESULT_TYPE,
  createInMemorySearchProviders,
  createSearchService,
  searchArticles,
  searchProfiles,
  validateSearchQuery
} from "./index.js";
import { createSearchService as rootCreateSearchService } from "../index.js";

describe("search public exports", () => {
  it("exports the public search API", () => {
    expect(ARTICLE_RESULT_TYPE).toBe("article");
    expect(PROFILE_RESULT_TYPE).toBe("profile");
    expect(createInMemorySearchProviders).toBeTypeOf("function");
    expect(createSearchService).toBeTypeOf("function");
    expect(searchArticles).toBeTypeOf("function");
    expect(searchProfiles).toBeTypeOf("function");
    expect(validateSearchQuery).toBeTypeOf("function");
    expect(rootCreateSearchService).toBe(createSearchService);
  });
});
