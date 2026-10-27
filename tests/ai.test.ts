import { describe, it, expect, vi } from "vitest";
import { explain } from "../server/ai";
describe("Saarthi explanations", () => {
  it.each(["en", "ta", "hi"] as const)(
    "provides a text fallback in %s",
    async (language) => {
      vi.stubEnv("GEMINI_API_KEY", "");
      const r = await explain("pay", language);
      expect(r.source).toBe("fallback");
      expect(r.explanation.length).toBeGreaterThan(50);
      vi.unstubAllEnvs();
    },
  );
  it("falls back when Gemini fails", async () =>
    expect(
      (
        await explain("safety", "en", {}, async () => {
          throw new Error("Unavailable");
        })
      ).source,
    ).toBe("fallback"));
  it("falls back for invalid structured output", async () =>
    expect(
      (await explain("rest", "ta", {}, async () => '{"invented":"unsafe"}'))
        .source,
    ).toBe("fallback"));
  it("validates structured output", async () =>
    expect(
      (
        await explain("cases", "hi", {}, async () =>
          JSON.stringify({
            explanation: "A valid explanation.",
            nextAction: "Open cases.",
          }),
        )
      ).source,
    ).toBe("gemini"));
});
