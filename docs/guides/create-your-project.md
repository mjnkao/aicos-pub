# Create Your Own AICOS Project

Status: public staging guide

## Goal

Use AICOS to give agents a compact, role-aware context layer for your existing
project.

## Step 1 - Choose Project Identity

Define:

- project id;
- project name;
- source repo path;
- primary branch;
- active workstream;
- project-facing roles.

Example:

```text
project_id: customer-support-digest
project_name: Customer Support Digest
source_repo: ../customer-support-digest
primary_branch: main
active_workstream: daily-support-summary
roles: product-owner, cto, fullstack-dev, reviewer, operator
```

## Step 2 - Define Authority Boundaries

Your source repo owns:

- code;
- tests;
- scripts;
- schemas;
- generated artifacts;
- source provenance.

AICOS owns:

- compact project digests;
- working state;
- role-aware context ladders;
- task packets;
- handoffs;
- checkpoints;
- open items, questions, and risks.

## Step 3 - Create Compact Canonical Digests

Start with:

- project profile;
- project brief;
- architecture baseline;
- source and data scope;
- delivery baseline.

Keep these short. Do not paste the whole source repo or long history.

## Step 4 - Create Working State

Add:

- current state;
- current direction;
- open items;
- open questions;
- active risks;
- current handoff stub.

## Step 5 - Create Role-Aware Context Ladder

Define what each role reads first.

CEO, product owner, CTO, dev, reviewer, and operator should not receive the same
startup bundle.

## Step 6 - Create One Workstream

Pick one active workstream. Keep it small enough that a new agent can understand
the slice quickly.

## Step 7 - Create One Task Packet

Only create a task packet after there is a real task.

The packet should specify:

- objective;
- required context;
- allowed write lanes;
- source artifacts;
- acceptance criteria;
- handoff expectations.

## Step 8 - Connect Agents Through AICOS

Agents should read AICOS context first, then inspect the source repo only for
the selected task.
