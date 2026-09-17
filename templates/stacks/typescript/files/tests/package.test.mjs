import assert from "node:assert/strict";
import test from "node:test";
import { projectStatus } from "../src/index.ts";

test("the TypeScript entrypoint loads", () => {
  assert.equal(projectStatus, "initialized");
});
