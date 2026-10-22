# Goal Todo Template

Use this exact structure for generated TODO documents.

```markdown
# Todo for <Spec Title>

Source spec: `<relative/path/to/spec.md>`

## Todo
### <Task Type or Feature Area>
- [ ] [Logic] Implement **required rule** for the target workflow.
- [ ] [UI] Build **required screen state** for the target user flow.
- [ ] [Data] Add **required data contract** for persistence or integration.
```

## Category guide

- `[Logic]` — business rules, gameplay rules, control flow, validation, state machines, service behavior, command handlers, events.
- `[UI]` — screens, components, layout, visual states, interaction states, navigation, accessibility, animation, localization display.
- `[Data]` — schemas, saved state, migrations, assets, localization tables, analytics payloads, config, external API/request contracts.

## Grouping guide

- Use task type groups such as `### Logic`, `### UI`, and `### Data` for compact specs.
- Use related feature groups such as `### Cart Totals` or `### Checkout Recovery` when the spec spans multiple flows.
- Keep each TODO item in the group where an implementer would naturally start work.

## Quality bar

A good TODO item is concrete enough that a different agent can implement it without rereading the entire spec for intent.
