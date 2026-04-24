import { scoreFullTextRecord, sortByRelevanceThenId } from "./fullText.js";
import { PROFILE_RESULT_TYPE } from "./searchTypes.js";
import { validateSearchQuery } from "./validateSearchQuery.js";

const PROFILE_FIELDS = Object.freeze([
  { name: "displayName", weight: 5 },
  { name: "username", weight: 4 },
  { name: "bio", weight: 2 }
]);

export function searchProfiles({ query, profiles }) {
  const validation = validateSearchQuery(query);

  if (!validation.ok) {
    return [];
  }

  return [...(profiles ?? [])]
    .map((profile) => toProfileSearchResult({ profile, validation }))
    .filter((result) => result.score > 0)
    .sort(sortByRelevanceThenId);
}

function toProfileSearchResult({ profile, validation }) {
  const relevance = scoreFullTextRecord({
    record: profile,
    fields: PROFILE_FIELDS,
    terms: validation.terms,
    query: validation.query
  });

  return {
    type: PROFILE_RESULT_TYPE,
    id: profile.id,
    username: profile.username,
    displayName: profile.displayName,
    bio: profile.bio ?? "",
    url: profile.url ?? `/profiles/${profile.username ?? profile.id}`,
    score: relevance.score,
    matchedFields: relevance.matchedFields
  };
}
