---
name: git-resolve
description: "Use this skill to process GitHub Pull Request review comments one at a time: read each comment, investigate whether it is valid, fix valid findings, commit each fix separately, reply with the resolution reason, and resolve the review thread. Use it when the user says to resolve PR review comments, fix reviewer feedback, address review comments, or investigate comments on a PR."
metadata:
  author: kuozg
  version: "1.0"
---
# git-resolve

Resolve GitHub Pull Request review comments by investigating each thread, fixing valid feedback, committing that fix alone, and replying with the reason before resolving the thread.

## When to Use

- Addressing inline review comments on a GitHub PR
- Fixing reviewer feedback after a code review
- Investigating whether PR comments are correct before changing code
- Resolving review threads with a written explanation

## Workflow

1. **Identify** - Determine the PR number and base branch from the user, `gh pr status`, or `gh pr view`
2. **Fetch comments** - List unresolved review threads and include comment body, author, path, line, diff hunk, and thread ID
3. **Snapshot state** - Run `git status --short` and note unrelated dirty files before editing
4. **Process one thread** - Pick one unresolved comment thread and read the referenced file, surrounding code, and relevant call sites
5. **Judge validity** - Decide whether the comment is correct, partially correct, obsolete, or incorrect based on code evidence
6. **Fix valid feedback** - Make the smallest scoped change that addresses that one comment only
7. **Verify** - Run the narrowest meaningful test, lint, typecheck, build, or manual inspection for that fix
8. **Commit** - Stage only files changed for that comment and create one commit for that comment
9. **Reply** - Comment on the review thread with the reason for the resolution, including what changed or why no code change was needed
10. **Resolve** - Resolve the review thread after the explanatory reply is posted
11. **Repeat** - Move to the next unresolved thread only after the current thread is committed, replied to, and resolved

## GitHub Commands

Use `gh` where possible and GraphQL when thread IDs are needed.

Fetch PR metadata:

```bash
gh pr view <pr> --json number,title,baseRefName,headRefName,url
```

Fetch unresolved review threads:

```bash
gh api graphql -f query='
query($owner:String!, $repo:String!, $pr:Int!) {
  repository(owner:$owner, name:$repo) {
    pullRequest(number:$pr) {
      reviewThreads(first:100) {
        nodes {
          id
          isResolved
          path
          line
          comments(first:20) {
            nodes {
              id
              author { login }
              body
              url
              diffHunk
            }
          }
        }
      }
    }
  }
}' -F owner=<owner> -F repo=<repo> -F pr=<pr>
```

Reply to a review thread:

```bash
gh api graphql -f query='
mutation($thread:ID!, $body:String!) {
  addPullRequestReviewThreadReply(input:{pullRequestReviewThreadId:$thread, body:$body}) {
    comment { url }
  }
}' -F thread=<thread_id> -f body='<reason>'
```

Resolve a review thread:

```bash
gh api graphql -f query='
mutation($thread:ID!) {
  resolveReviewThread(input:{threadId:$thread}) {
    thread { id isResolved }
  }
}' -F thread=<thread_id>
```

## Rules

- One review comment thread equals one focused work item
- One valid fix equals one commit; never batch multiple review comments into a single commit
- If a thread has multiple comments about the same issue, treat the thread as one work item
- Do not create a code commit for an obsolete or incorrect comment unless a real code change is still needed
- Always reply with the resolution reason before resolving the thread
- The reply must state whether the comment was valid, what changed, the verification run, and the commit hash when a commit was created
- Preserve unrelated dirty files; stage explicit paths only
- Do not rewrite existing commits, force-push, or push unless the user explicitly asks
- Do not resolve a thread if verification failed or if the investigation is inconclusive; leave a reply explaining the blocker instead
- If a comment asks for a broad refactor that affects multiple concerns, split only when the review thread clearly contains independent issues; otherwise keep the commit scoped to that thread

## Reply Format

For a fixed valid comment:

```text
Resolved as valid.

Reason: <why the review comment was correct>
Change: <what was changed>
Verification: <command or check and result>
Commit: <short_sha> <commit subject>
```

For an obsolete or incorrect comment:

```text
Resolved without code change.

Reason: <code evidence showing why the comment no longer applies or is incorrect>
Verification: <inspection or command used>
```

For a blocked comment:

```text
Not resolved yet.

Reason: <what is unclear or failing>
Next step: <specific information or fix needed>
```

## Output Format

Final response should list each processed thread with status, commit hash if any, verification evidence, and whether the GitHub thread was resolved.
