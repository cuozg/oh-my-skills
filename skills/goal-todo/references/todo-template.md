# Goal Todo Template

Use this exact structure for generated TODO documents.

```markdown
# Todo for <Spec Title>

Source spec: `<relative/path/to/spec.md>`

## Todo
- [ ] [Logic] Implement **required rule** for the target workflow.
- [ ] [UI] Build **required screen state** for the target user flow.
- [ ] [Data] Add **required data contract** for persistence or integration.

## Test cases
- [ ] Verify **expected behavior** for the completed requirement.
- [ ] Verify **required edge state** returns the expected result.
```

## Category guide

- `[Logic]` — business rules, gameplay rules, control flow, validation, state machines, service behavior, command handlers, events.
- `[UI]` — screens, components, layout, visual states, interaction states, navigation, accessibility, animation, localization display.
- `[Data]` — schemas, saved state, migrations, assets, localization tables, analytics payloads, config, external API/request contracts.

## Quality bar

A good TODO item is concrete enough that a different agent can implement it without rereading the entire spec for intent. A good test case is concrete enough that a different agent can prove pass/fail without inventing the expected result.
