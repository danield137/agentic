# Handbooks

A handbook is an onboarding companion for a large codebase. It introduces the
ideas a newcomer must hold in their head, such as the product's core concepts,
main flows, and cross-cutting concerns, and shows where each one lives, without
explaining every detail.

## Profile

| Dimension | Handbook |
| --- | --- |
| Reader | An engineer who knows software engineering but not this product or its domain. |
| Question | What should I understand? |
| Language | Plain engineering English that any computer science graduate can follow. Define domain terms at first use. Avoid specialist terms, such as graph theory, retrieval, or PCA, unless the concept is central to the product. |
| Coverage | Broad. Every concept a newcomer needs, including ones that aren't components or algorithms. A banking handbook covers transactions, data recovery, and security, and how each shows up in the product. |
| Depth | Conceptual. Rough step-by-step outlines and landmarks: the service, folder, or table where something lives. No schemas, signatures, class structure, or call chains. |
| Intent | Build intuition, so the reader can find their way around and ask good questions. |
| Length | One topic per page or section, readable in a few minutes. |
| Stop when | The next sentence would name a column, method, class, or configuration key, or describe caching, memory use, concurrency, retries, or performance tuning. Link to the architecture doc or the code instead. |

## Guidelines

- Organize by concept, not by component or folder. One concept, such as
  transactions, can span several services; say how it shows up in each.
- Open each topic with why it matters to this product, then how it works in
  broad strokes, then where to look.
- Describe flows as rough step-by-step outlines: numbered, plain verbs, one idea
  per step.
- Give landmarks, not maps. "Recipe connections are stored in the
  `recipe_links` table" is enough; leave out its columns.
- Use the codebase's real names for services, folders, and tables, verified
  against the repository, so the reader can search for them.
- Link down to the architecture doc, ADRs, specs, and code. Link across to
  related topics. Don't copy their content.
- Start with an index that lists the topics, each with a one-line summary of
  what the reader will understand. When the handbook outgrows one file, give
  each topic its own page and keep the index as the entry page.
- Put open questions and todos at the bottom of the topic they belong to.

## Good examples

**A topic told as a rough step-by-step outline** (recipe app, "Similar
recipes"):

> When someone opens a recipe, "Find similar recipes" suggests three others
> they might like.
>
> 1. Every ingredient is sorted into a category, such as fruit, vegetable, or
>    grain, and given a taste profile: how sweet, salty, sour, bitter, or
>    savory it is.
> 2. Recipes that share ingredients are connected to each other.
> 3. Each recipe connected to the open one is scored on shared ingredients,
>    similar taste, and similar prep time.
> 4. The three highest scores are shown.
>
> Ingredient categories are stored in the `ingredients` table and connections
> in the `recipe_links` table. The scoring code is in `similarity/score.py`.
> For how scores are computed and cached, see the similarity section of the
> architecture doc.

It works because it uses plain words and a numbered outline, gives landmarks
without schemas, and links down for the machinery.

**A concept that isn't a component** (banking app, "Transactions"):

> Money never appears or disappears. Every transfer is recorded as two matching
> entries: one account goes down by the amount, and another goes up by the same
> amount. This is called double-entry bookkeeping. Both entries are saved
> together or not at all, so a failed transfer leaves no trace. That is why
> every balance change goes through the Ledger service (`services/ledger`);
> nothing else writes balances. Because every balance can be recomputed from
> these entries, the same history is how we rebuild an account after an
> incident (see "Data recovery").

It works because it explains why the concept matters, defines the one domain
term it needs, and ends with a landmark and a link to a related topic.

**An index:**

> - **Transactions**: why money always moves in matching pairs, and the one
>   service allowed to move it.
> - **Data recovery**: how any balance can be rebuilt from history.
> - **Security**: who can see or move money, and where that is checked.

It works because each line promises one thing the reader will understand, and
the topics are concepts rather than folders.

## Bad examples

**Jargon and machinery:**

> Similarity is computed from PCA-reduced flavor embeddings over a bipartite
> recipe-ingredient graph, and top-k neighbors are served from a write-through
> Redis cache with a 24-hour TTL.

It fails because it jumps three levels at once, uses specialist terms a
newcomer doesn't need, and describes caching, which belongs in the architecture
doc.

**A schema dump:**

> `recipe_links(recipe_id TEXT, linked_recipe_id TEXT, shared_count INT,
> weight FLOAT, PRIMARY KEY (recipe_id, linked_recipe_id))`

It fails because the reader needs the landmark, that connections live in
`recipe_links`, not the columns. Schemas belong in the spec or the code.

**A call chain instead of a concept:**

> `TransferController.post()` calls `TransferService.execute()`, which calls
> `LedgerClient.postEntries()`, which opens a database transaction.

It fails because method-by-method flow is architecture or code detail. The
handbook should say what a transfer guarantees and where that guarantee is
enforced.

## Template

Use `assets/templates/handbook.md`.
