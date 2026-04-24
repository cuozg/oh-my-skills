import { scoreFullTextRecord, sortByRelevanceThenId } from "./fullText.js";
import { ARTICLE_RESULT_TYPE } from "./searchTypes.js";
import { validateSearchQuery } from "./validateSearchQuery.js";

const ARTICLE_FIELDS = Object.freeze([
  { name: "title", weight: 5 },
  { name: "body", weight: 2 }
]);

export function searchArticles({ query, articles }) {
  const validation = validateSearchQuery(query);

  if (!validation.ok) {
    return [];
  }

  return [...(articles ?? [])]
    .map((article) => toArticleSearchResult({ article, validation }))
    .filter((result) => result.score > 0)
    .sort(sortByRelevanceThenId);
}

function toArticleSearchResult({ article, validation }) {
  const relevance = scoreFullTextRecord({
    record: article,
    fields: ARTICLE_FIELDS,
    terms: validation.terms,
    query: validation.query
  });

  return {
    type: ARTICLE_RESULT_TYPE,
    id: article.id,
    slug: article.slug,
    title: article.title,
    excerpt: article.excerpt ?? createExcerpt(article.body),
    url: article.url ?? `/articles/${article.slug ?? article.id}`,
    score: relevance.score,
    matchedFields: relevance.matchedFields
  };
}

function createExcerpt(body) {
  const normalizedBody = String(body ?? "").trim();

  if (normalizedBody.length <= 160) {
    return normalizedBody;
  }

  return `${normalizedBody.slice(0, 157).trim()}...`;
}
