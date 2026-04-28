# Project Authority Split

Status: concept

## Core Idea

AICOS is the context/control-plane. Your project repo is the artifact/runtime
authority.

This prevents AICOS from becoming a raw mirror of every project while still
giving agents the context they need to work.

## AICOS Owns

- compact project truth;
- current working state;
- context ladders;
- role-aware startup routing;
- task packets;
- checkpoints;
- handoffs;
- open questions, risks, and decisions.

## The Project Repo Owns

- code;
- tests;
- runtime configs;
- scripts;
- source data;
- generated output;
- artifact provenance.

## Promotion

Raw evidence becomes AICOS context only after review and promotion into compact
canonical or working files.
