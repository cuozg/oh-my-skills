export const searchFixtures = {
  articles: [
    {
      id: "article-published",
      slug: "full-text-search",
      title: "Full Text Search",
      body: "Build full text search across articles and people.",
      status: "published",
      visibility: "public"
    },
    {
      id: "article-draft",
      slug: "draft-search",
      title: "Draft Search",
      body: "This draft should stay outside search.",
      status: "draft",
      visibility: "public"
    }
  ],
  profiles: [
    {
      id: "profile-public",
      username: "searchperson",
      displayName: "Full Text Person",
      bio: "Profile for full text search discovery.",
      visibility: "public"
    },
    {
      id: "profile-private",
      username: "private-search",
      displayName: "Private Search",
      bio: "Private profile should not be returned.",
      visibility: "private"
    }
  ]
};
