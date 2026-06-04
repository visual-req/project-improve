#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import process from "node:process";
import { spawn } from "node:child_process";

function usage() {
  const text = [
    "prjmx",
    "",
    "Commands:",
    "  prjmx init --project-id <id>           Create work directories for a project",
    "  prjmx frontend                         Install deps (if needed) and start frontend dev server",
    "",
    "Examples:",
    "  npx . init --project-id proj-123",
    "  npx . frontend"
  ].join("\n");
  process.stdout.write(text + "\n");
}

function getArg(name) {
  const idx = process.argv.indexOf(name);
  if (idx === -1) return null;
  const value = process.argv[idx + 1];
  if (!value || value.startsWith("-")) return null;
  return value;
}

function ensureDir(p) {
  fs.mkdirSync(p, { recursive: true });
}

function run(cmd, args, cwd) {
  return new Promise((resolve) => {
    const child = spawn(cmd, args, { cwd, stdio: "inherit", shell: process.platform === "win32" });
    child.on("exit", (code) => resolve(code ?? 0));
  });
}

const command = process.argv[2];

if (!command || command === "-h" || command === "--help") {
  usage();
  process.exit(0);
}

const root = process.cwd();

if (command === "init") {
  const projectId = getArg("--project-id") || getArg("-p");
  if (!projectId) {
    process.stderr.write("Missing --project-id\n");
    usage();
    process.exit(1);
  }

  const inputsDir = path.join(root, "work", "inputs", projectId);
  const outputsDir = path.join(root, "work", "outputs", projectId, "project-metrics-orid");
  const metaDir = path.join(root, "work", "meta", projectId);

  ensureDir(inputsDir);
  ensureDir(outputsDir);
  ensureDir(metaDir);

  process.stdout.write(`Created:\n- ${inputsDir}\n- ${outputsDir}\n- ${metaDir}\n`);
  process.exit(0);
}

if (command === "frontend") {
  const frontendDir = path.join(root, "frontend");
  const nodeModules = path.join(frontendDir, "node_modules");
  if (!fs.existsSync(frontendDir)) {
    process.stderr.write("frontend/ directory not found\n");
    process.exit(1);
  }

  (async () => {
    if (!fs.existsSync(nodeModules)) {
      const code = await run("npm", ["install"], frontendDir);
      if (code !== 0) process.exit(code);
    }
    const code = await run("npm", ["run", "dev"], frontendDir);
    process.exit(code);
  })();
}

process.stderr.write(`Unknown command: ${command}\n`);
usage();
process.exit(1);
