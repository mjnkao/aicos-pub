# Security Policy

Status: public staging draft

## Reporting

Do not open public issues with secrets, credentials, private project context, or
personal data.

For now, report sensitive issues privately to the repository maintainer.

## Sensitive Data

Never commit:

- API keys;
- tokens;
- passwords;
- private keys;
- `.env` files;
- local MCP client configs with credentials;
- private handoffs or checkpoints;
- user/customer/project data;
- generated logs or runtime dumps.

## Public Examples

All examples should be synthetic and safe to share publicly.

If an example is derived from a real project, rewrite it into a neutral sample
with fake names, fake paths, fake source inputs, and no operational history.
