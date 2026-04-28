# Task Packet Lifecycle

Status: concept

## Purpose

A task packet gives an agent the smallest useful bundle of context and rules for
one selected task.

## Lifecycle

1. Draft packet when a real task is selected.
2. Include objective, role, source artifacts, required context, and allowed
   write lanes.
3. Agent executes the task.
4. Agent records meaningful checkpoints or handoff.
5. Packet becomes completed, retired, or replaced.

## Do Not

- load all packets at startup;
- keep stale packets as active tasks;
- use task packets as chat logs;
- include secrets or raw private evidence;
- turn every small command into a checkpoint.
