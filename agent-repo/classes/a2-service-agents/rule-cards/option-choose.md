# Rule Card: Option Choose

Load when a human/manager selects an option in chat or review flow.

## Command

```text
./aicos option choose <project-id> <blocker-id> <option-id>
```

## Use When

- human clearly chooses an option
- human selects an execution branch
- blocker now has a committed direction

## Updates

- human approval packet
- selected branch state
- project working state/direction
- blocker or open-question status when relevant

## Never

- promote canonical truth
- delete other options
- replace human choice with agent recommendation
- treat this command as a chat UI
