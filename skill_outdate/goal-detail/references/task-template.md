# Detail Document Template

Use this structure for the file written to
`Docs/Goals/{feature-name}/detail/{kebab-case-task}.md`.

```markdown
# {Goal title} — Detail

Source goal: `Docs/Goals/{feature-name}/{kebab-case-task}.md`
Parent spec: `Docs/Features/{feature-name}/TacticsModeGDD.md` (or equivalent)
Parent todo: `Docs/Features/{feature-name}/TacticsMode-todo.md` (if present)

## Architecture split

Skip this section if the goal lives entirely on client or entirely on server.
Otherwise, fill a 2-column table: Concern | Owner (SERVER / CLIENT / BOTH).

## Verified anchors

Cite exact file:line for every existing class/method/field the Tasks touch.
Re-verify each one against the current source before writing.

---

## Task 1: T-{n} — {REPO}: {one-line title}

**Files:**
- Create: `/abs/path/to/NewFile.cs`
- Modify: `/abs/path/to/Existing.cs:{line}` — what is being changed

**Interfaces:**
- Consumes: `ExistingType` (Task X) — what it provides
- Produces:
  - `public Type NewMember` — one-line description

- [ ] **Step 1: {verb + target}**

```csharp
// Code block, file-anchored with a leading comment showing the target file
```

- [ ] **Step 2: Verify**

```bash
dotnet build /abs/path/Project.csproj
# Expected: <observable outcome>
```

- [ ] **Step 3: Commit**

```bash
cd /abs/path/to/repo
git add <files>
git commit -m "{imperative subject}"
```

**Acceptance:**
- One bullet per testable outcome (one line each).
- Every bullet must be independently verifiable by a fresh agent.

---

## Task 2: T-{n}-mirror — CLIENT: {title}
(same shape as Task 1)

---

## Cross-Repo Notes

Use this section when work spans both repos. List each shared artifact
(enum value, JSON parser field, wire format) and the exact files on both sides
that must stay in lock-step.

## Verification

Final invariants the whole detail doc must satisfy after every Task lands.
Numbered, one line each. An agent should be able to grep these to confirm
the detail doc is fully complete.
```

## Task-id convention

- `T-1`, `T-2`, ... — main Tasks on the primary repo.
- `T-1-mirror` — client mirror of a server Task.
- `T-1-parse` — wire-format parser side.
- `T-1-test` — dedicated test project Task (rare; tests usually live in the
  Task they verify).

## Verb density

Each Step is one logical change. Each Task is one commit. A fresh agent should
be able to ship a Task in a single session without asking follow-up questions.
