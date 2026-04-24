export function createInMemorySearchProviders({
  articles = [],
  profiles = [],
  isArticleSearchable = defaultArticleSearchable,
  isProfileSearchable = defaultProfileSearchable
} = {}) {
  return {
    async getSearchableArticles() {
      return articles.filter(isArticleSearchable).map(copyRecord);
    },
    async getSearchableProfiles() {
      return profiles.filter(isProfileSearchable).map(copyRecord);
    }
  };
}

export function defaultArticleSearchable(article) {
  return (
    article?.searchable !== false &&
    (article?.status === undefined || article.status === "published") &&
    (article?.visibility === undefined || article.visibility === "public")
  );
}

export function defaultProfileSearchable(profile) {
  return (
    profile?.searchable !== false &&
    (profile?.visibility === undefined || profile.visibility === "public")
  );
}

function copyRecord(record) {
  return { ...record };
}
