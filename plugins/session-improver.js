/**
 * Session Improver Plugin
 *
 * Fires after each session goes idle (agent finishes responding).
 * It queues a retrospective that analyzes what the session accomplished
 * and uses that to improve relevant skills and standards — so the next
 * time a similar task runs, the agent does it better.
 *
 * The retrospective runs as a background subtask so it never blocks
 * the user's next interaction.
 */

// Track sessions we've already triggered a retrospective for, so we
// don't fire multiple times on repeated idle events in the same session.
const processedSessions = new Set();

// Debounce map: sessionID → timeout handle.
// We wait a short window after the last idle event before firing so
// we don't trigger mid-stream oscillations.
const debounceHandles = new Map();
const DEBOUNCE_MS = 3000; // 3 seconds quiet window

export const SessionImproverPlugin = async ({ client, $ }) => {
  return {
    event: async ({ event }) => {
      // Only act on session.idle — this fires when the AI has finished
      // generating its response for a turn.
      if (event.type !== "session.idle") return;

      const sessionID = event.properties?.sessionID;
      if (!sessionID) return;

      // Skip if we already fired the retrospective for this session.
      if (processedSessions.has(sessionID)) return;

      // Debounce: reset the timer every time idle fires.
      if (debounceHandles.has(sessionID)) {
        clearTimeout(debounceHandles.get(sessionID));
      }

      const handle = setTimeout(async () => {
        debounceHandles.delete(sessionID);

        // Mark as processed BEFORE the async work to prevent re-entry.
        processedSessions.add(sessionID);

        try {
          await client.app.log({
            body: {
              service: "session-improver",
              level: "info",
              message: `Triggering post-session retrospective for session ${sessionID}`,
              extra: { sessionID },
            },
          });

          // Inject the retrospective command into the TUI prompt.
          // This appends "/omo/retrospective" as a new message in the
          // current session so Sisyphus can analyse what was done and
          // improve the relevant skills in the background.
          await client.tui.prompt.append({
            body: {
              sessionID,
              text: "/omo/retrospective",
            },
          });
        } catch (err) {
          await client.app.log({
            body: {
              service: "session-improver",
              level: "warn",
              message: `Failed to trigger retrospective: ${err?.message ?? err}`,
              extra: { sessionID },
            },
          });
        }
      }, DEBOUNCE_MS);

      debounceHandles.set(sessionID, handle);
    },
  };
};
