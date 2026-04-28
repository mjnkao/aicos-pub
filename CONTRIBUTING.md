# Contributing

Status: public staging draft

## Principles

- Keep AICOS local-first and human-readable.
- Prefer compact project context over raw repository mirrors.
- Keep private data out of public examples and tests.
- Make role and authority boundaries explicit.
- Add small, reviewable changes.

## Public Example Rules

Examples must use synthetic data. Do not submit real:

- project handoffs;
- user logs;
- customer data;
- credentials;
- private source inventories;
- generated runtime bundles;
- trading, financial, medical, legal, or other sensitive personal context.

## Development Flow

1. Create a branch.
2. Make a focused change.
3. Run scans for private markers and secrets.
4. Update docs or examples when behavior changes.
5. Open a pull request with the problem, change, and verification.

## Before Opening A PR

Check:

- no `.env` files;
- no local absolute paths;
- no private project names;
- no generated output bulk;
- no logs or handoff history;
- examples are synthetic.
- daemon docs/examples keep tokens as placeholders only.
