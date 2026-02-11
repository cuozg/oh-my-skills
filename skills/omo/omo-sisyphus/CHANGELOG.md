# Changelog

## v3.5.0 Update (2026-02-11)

Aligned with oh-my-opencode v3.5.0 "Atlas Trusts No One" (2026-02-10).

### Added
- **Atlas manual review constraint**: Delegated prompts must instruct subagents to `Read` all modified files before completion
- **Boulder continuation for Sisyphus**: Sisyphus sessions can now participate in boulder continuation (previously Atlas-only)
- **v3.5.0 Enhancements section**: Documents new capabilities (boulder continuation, TaskCreate/Update/List, @path resolution, session ID validation)
- **File read verification**: Added to Checklist, MUST DO, and delegation template
- **Session ID validation guidance**: Anti-pattern for unvalidated session IDs
- **Sisyphus-Junior TaskCreate/Update/List note**: Added to Skill Selection table

### Changed
- Updated frontmatter description to reference Atlas review and boulder continuation
- Enhanced Hard Constraints table with 2 new rows (Atlas review, boulder continuation)
- Updated Generate Prompt step to include file read requirement
- Updated delegation template MUST DO with `Read` requirement
- Extended Anti-Patterns table with 3 new entries

### No Breaking Changes
- All existing delegation patterns remain valid
- No constraint restrictions were removed or weakened
