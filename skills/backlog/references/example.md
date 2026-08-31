# Backlog

Simple planning for adding document search. Start with the design document for context.

Important: PR 42 is a reference implementation, not the baseline. New work should start from the repository's default branch. Use the prototype for ideas and experiments only.

---

* (current) [ ] **M1:** Stabilize the search foundation
  * [ ] **M1T1:** Finalize a versioned index format
    * Note: Preserve forward compatibility and support deterministic random lookup.
  * [ ] **M1T2:** Define relevance and latency benchmarks
    * Note: Record result quality, query latency, index size, and build time.
  * [ ] **M1T3:** Validate malformed, empty, and unsupported input

* (next) [ ] **M2:** Build indexing and query paths
  * [ ] **M2T1:** Build indexes during ingestion
  * [ ] **M2T2:** Query indexes with an exact fallback
    * Note: Missing, corrupt, or skipped indexes must preserve correct results.
  * [ ] **M2T3:** Cache shared metadata instead of reopening it per query

* (future) [ ] **M3:** Expose the feature
  * [ ] **M3T1:** Add user-facing configuration behind a feature flag
  * [ ] **M3T2:** Document rollout, limitations, and benchmark expectations

---

## Archive

Finished milestones are appended here, newest last.
