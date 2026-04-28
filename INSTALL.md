# Install AICOS

Status: public staging guide

This guide is for a new user cloning AICOS locally for the first time.

## Requirements

- macOS or Linux shell
- `python3`
- `git`
- optional: an MCP-capable agent client such as Codex, Claude Code, Gemini CLI,
  or another local MCP client

AICOS currently uses Python standard-library code for the exported kernel and
CLI path. No package install is required for the basic CLI help check.

## Clone

```bash
git clone <AICOS_REPO_URL> aicos
cd aicos
```

If you already have a local checkout, enter that checkout:

```bash
cd <AICOS_CHECKOUT>
```

## Verify The CLI

Run:

```bash
./aicos --help
```

Expected result:

```text
usage: aicos [-h] {capsule,branch,option,promote,validate,context,sync,mcp,compact} ...
```

If `./aicos` is not executable, run:

```bash
chmod +x ./aicos
```

## Verify Python Files

Run:

```bash
PYTHONPYCACHEPREFIX=/tmp/aicos-pycache \
  python3 -m py_compile packages/aicos-kernel/aicos_kernel/*.py
```

No output means the compile check passed.

## Explore The Sample Project

Run:

```bash
find examples/sample-project -type f | sort
```

Start with:

```text
examples/sample-project/README.md
examples/sample-project/brain/project/canonical/project-profile.md
examples/sample-project/brain/project/working/context-ladder.md
examples/sample-project/workstreams/default-digest-slice.md
examples/sample-project/task-packets/README.md
```

## Create Your Own Project Context

Copy the sample:

```bash
mkdir -p my-aicos-context
cp -R examples/sample-project/* my-aicos-context/
```

Then replace:

```text
sample-project -> your-project-id
Sample Research Digest -> Your Project Name
```

Follow:

```text
docs/guides/create-your-project.md
```

## Optional: Local MCP Bridge

The local MCP bridge is in:

```text
integrations/local-mcp-bridge/
```

Generic MCP command shape:

```text
python3 <AICOS_REPO_PATH>/integrations/local-mcp-bridge/aicos_mcp_stdio.py
```

For this checkout:

```bash
python3 integrations/local-mcp-bridge/aicos_mcp_stdio.py
```

Your MCP client should configure that command as a local stdio server.

## Optional: HTTP MCP Daemon

For local desktop or trusted-LAN HTTP access, use:

```text
docs/guides/mcp-daemon-local-setup.md
```

That path includes:

- `scripts/aicos-bootstrap-full`
- `scripts/aicos-daemon-start`
- `integrations/mcp-daemon/start-lan.sh`
- `scripts/aicos-install-launchagents`

## Safety Check Before Sharing

Before making a repo public, run scans for private markers:

```bash
rg -n --hidden --glob '!.git/**' -i \
  '/Users/|\\.env|private key|token|secret|handoff|checkpoint|generated output bulk' .
```

Review results manually. Some words may appear in safety docs, but real private
paths, secrets, logs, or project data should not be present.

## Current Limitations

- No packaged installer yet.
- MCP client setup is manual.
- Public examples are synthetic.
- Role-aware context APIs are still design-stage.
- The private source export allowlist still needs to include the new daemon helper files.
- This staging package is not yet a final release.
