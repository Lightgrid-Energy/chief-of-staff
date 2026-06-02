# /my-tasks — Task Management

Manages the task list at `~/.claude/my-tasks.yaml`.

## Operations

### `/my-tasks` — List tasks
Display all active tasks grouped by urgency:
1. Overdue
2. Due today
3. Due this week
4. Later

For each: ID, title, priority, due date, goal alignment, status.

### `/my-tasks add` — Add a task
Prompt for:
- Title (required)
- Description (optional)
- Due date (required — use approximate if unsure: "end of week", "end of month")
- Priority (1-4)
- Goal alignment (which OBJ does this support?)

Generate next available TASK-ID. Write to my-tasks.yaml.

### `/my-tasks done [ID]` — Complete a task
Mark task as complete, add completion date. Confirm: "Mark TASK-XXX complete?"

### `/my-tasks execute` — Work on top task
1. Identify the highest-priority pending task
2. Read it carefully
3. Present a plan: what you'll do, what you need
4. Execute: draft the email, do the research, write the doc — whatever the task requires
5. Present output for review
6. Ask "Should I mark [TASK-ID] complete?"

## Background Behavior

At the start of each substantive session, silently check tasks and surface only:
- Tasks that are overdue
- Tasks due today
- Tasks marked "blocked" with no recent update

Don't interrupt if nothing is critical. One line max: "⚠️ TASK-002 is overdue — want to address it?"

## Design Rules

- Every task needs a due date (approximate is fine)
- Every task should align to a goal OBJ (flag if it doesn't — let Mujtaba decide)
- Claude helps execute — Mujtaba marks complete
- Finishing early is a win — look for opportunities to advance tasks ahead of schedule
