#!/usr/bin/env python3
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SYNC = ROOT / "scripts" / "sync.py"
HOOK = ROOT / "scripts" / "deny_read_hook.py"
sys.path.insert(0, str(ROOT / "scripts"))

import deny_read_hook  # noqa: E402
import sync  # noqa: E402


class TokenMapping(unittest.TestCase):
    def setUp(self):
        self.h = Path("/Users/ada")
        self.policy = sync.Policy(
            path=Path("/tmp/policy.toml"),
            deny_reads=["~/.secrets/**", "**/.env", "/etc/shadow"],
            deny_writes=["~/.secrets/**"],
            deny_commands=["rm -rf *", "sudo *"],
        )

    def test_claude_keeps_tilde_and_double_slash(self):
        toks = sync.tokens_for("claude", self.policy, self.h)
        self.assertIn("Read(~/.secrets/**)", toks)
        self.assertIn("Read(//**/.env)", toks)
        self.assertIn("Read(//etc/shadow)", toks)
        self.assertIn("Edit(~/.secrets/**)", toks)
        self.assertIn("Write(~/.secrets/**)", toks)
        self.assertIn("Bash(rm -rf *)", toks)

    def test_grok_uses_absolute_home(self):
        toks = sync.tokens_for("grok", self.policy, self.h)
        self.assertIn("Read(/Users/ada/.secrets/**)", toks)
        self.assertIn("Read(**/.env)", toks)
        self.assertIn("Read(/etc/shadow)", toks)
        self.assertIn("Edit(/Users/ada/.secrets/**)", toks)
        self.assertIn("Bash(sudo *)", toks)
        self.assertFalse(any(t.startswith("Read(~/") for t in toks))
        self.assertFalse(any("//**" in t for t in toks))

    def test_cursor_coarsens_shell(self):
        toks = sync.tokens_for("cursor", self.policy, self.h)
        self.assertIn("Read(/Users/ada/.secrets/**)", toks)
        self.assertIn("Write(/Users/ada/.secrets/**)", toks)
        self.assertIn("Shell(rm)", toks)
        self.assertIn("Shell(sudo)", toks)
        self.assertNotIn("Bash(rm -rf *)", toks)


class TomlUpsert(unittest.TestCase):
    def test_appends_missing_table(self):
        out = sync.upsert_toml_string_array("foo = 1\n", "permission", "deny", ["Read(a)"])
        self.assertIn("[permission]", out)
        self.assertIn('"Read(a)"', out)
        self.assertIn("foo = 1", out)

    def test_merges_existing_array(self):
        src = '[permission]\nallow = ["Bash(git *)"]\ndeny = [\n  "Read(old)",\n]\n'
        out = sync.upsert_toml_string_array(src, "permission", "deny", ["Read(old)", "Read(new)"])
        self.assertIn('"Read(old)"', out)
        self.assertIn('"Read(new)"', out)
        self.assertIn('"Bash(git *)"', out)
        self.assertEqual(out.count("Read(old)"), 1)

    def test_inserts_key_into_existing_table(self):
        src = '[permission]\nallow = ["Read"]\n'
        out = sync.upsert_toml_string_array(src, "permission", "deny", ["Read(x)"])
        self.assertIn("deny =", out)
        self.assertIn('"Read(x)"', out)
        self.assertIn("allow =", out)


class HookMatch(unittest.TestCase):
    def test_home_tree(self):
        secrets = str(Path.home() / ".secrets" / "token")
        self.assertTrue(deny_read_hook.match(secrets, "~/.secrets/**"))
        self.assertTrue(deny_read_hook.match(str(Path.home() / ".secrets"), "~/.secrets/**"))
        self.assertFalse(deny_read_hook.match(str(Path.home() / ".profile"), "~/.secrets/**"))

    def test_env_globs(self):
        self.assertTrue(deny_read_hook.match("/tmp/app/.env", "**/.env"))
        self.assertTrue(deny_read_hook.match("/tmp/app/.env.local", "**/.env.*"))
        self.assertFalse(deny_read_hook.match("/tmp/app/env.py", "**/.env"))
        self.assertTrue(deny_read_hook.match("/tmp/certs/foo.pem", "**/*.pem"))


class EndToEnd(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.h = Path(self.tmp.name) / "home"
        self.h.mkdir()
        self.cfg = Path(self.tmp.name) / "config"
        self.env = {
            **os.environ,
            "HOME": str(self.h),
            "XDG_CONFIG_HOME": str(self.cfg),
        }
        (self.h / ".claude").mkdir()
        (self.h / ".claude" / "settings.json").write_text(
            json.dumps({"permissions": {"allow": ["Read"], "deny": ["Bash(dd *)"]}}),
            encoding="utf-8",
        )
        (self.h / ".grok").mkdir()
        (self.h / ".grok" / "config.toml").write_text(
            '[ui]\npermission_mode = "always-approve"\n',
            encoding="utf-8",
        )
        (self.h / ".cursor").mkdir()

    def tearDown(self):
        self.tmp.cleanup()

    def run_sync(self, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, str(SYNC), *args],
            env=self.env,
            capture_output=True,
            text=True,
        )

    def test_init_status_apply(self):
        init = self.run_sync("init")
        self.assertEqual(init.returncode, 0, init.stderr)
        policy = Path(init.stdout.strip())
        self.assertTrue(policy.exists())

        st = self.run_sync("status")
        self.assertEqual(st.returncode, 1, st.stdout + st.stderr)
        self.assertIn("claude", st.stdout)
        self.assertIn("missing", st.stdout)

        dry = self.run_sync("apply")
        self.assertEqual(dry.returncode, 0, dry.stderr)
        self.assertIn("dry-run", dry.stderr)
        claude = json.loads((self.h / ".claude" / "settings.json").read_text())
        self.assertEqual(claude["permissions"]["deny"], ["Bash(dd *)"])

        wr = self.run_sync("apply", "--write", "--hooks")
        self.assertEqual(wr.returncode, 0, wr.stderr)
        claude = json.loads((self.h / ".claude" / "settings.json").read_text())
        self.assertIn("Read", claude["permissions"]["allow"])
        self.assertIn("Bash(dd *)", claude["permissions"]["deny"])
        self.assertIn("Read(~/.secrets/**)", claude["permissions"]["deny"])

        grok = (self.h / ".grok" / "config.toml").read_text()
        self.assertIn("permission_mode", grok)
        self.assertIn(f'Read({self.h}/.secrets/**)', grok)

        cursor = json.loads((self.h / ".cursor" / "cli-config.json").read_text())
        self.assertIn(f"Read({self.h}/.secrets/**)", cursor["permissions"]["deny"])
        self.assertIn("Shell(rm)", cursor["permissions"]["deny"])

        st2 = self.run_sync("status")
        self.assertEqual(st2.returncode, 0, st2.stdout + st2.stderr)

        # hook blocks a secrets path
        hook = subprocess.run(
            [sys.executable, str(HOOK)],
            env={**self.env, "AGENT_POLICY_FILE": str(policy)},
            input=json.dumps({"file_path": str(self.h / ".secrets" / "x")}),
            capture_output=True,
            text=True,
        )
        self.assertEqual(hook.returncode, 2, hook.stdout + hook.stderr)
        self.assertEqual(json.loads(hook.stdout)["permission"], "deny")

        # apply is idempotent
        wr2 = self.run_sync("apply", "--write")
        self.assertEqual(wr2.returncode, 0, wr2.stderr)
        claude2 = json.loads((self.h / ".claude" / "settings.json").read_text())
        self.assertEqual(
            claude2["permissions"]["deny"].count("Read(~/.secrets/**)"), 1
        )

        # never replace an existing regular guideline file
        existing = self.h / ".claude" / "rules" / "other.md"
        existing.parent.mkdir(parents=True, exist_ok=True)
        existing.write_text("# keep me\n", encoding="utf-8")
        src = policy.parent / "rules" / "secrets.md"
        how = sync.apply_guideline("claude", src, existing)
        self.assertEqual(how, "skipped-exists")
        self.assertEqual(existing.read_text(encoding="utf-8"), "# keep me\n")


if __name__ == "__main__":
    unittest.main()
