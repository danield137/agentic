# Specs

A spec defines a contract exactly: an API, a file or wire format, a
configuration schema, a command-line interface, or a protocol. It states what is
true, not why. Someone implementing either side of the contract, or a tool
checking it, should never need to ask a question.

## Profile

| Dimension | Spec |
| --- | --- |
| Reader | Implementers on either side of the contract, testers, and tools such as validators and client generators. |
| Question | Exactly what is the contract? |
| Language | Exact and normative. Use one term per concept and never vary wording for style. Use MUST, MUST NOT, SHOULD, and MAY as defined in RFC 2119 unless the repository has its own convention. |
| Coverage | Exhaustive within the declared surface: every operation or element, field, type, default, constraint, limit, and failure. State what is out of scope. |
| Depth | Enumerative. Names, types, formats, units, ranges, required or optional, defaults, ordering, idempotency, versioning, and every failure case. |
| Intent | Define, not explain. Reasons belong in the architecture doc or an ADR. |
| Length | As long as the surface requires, with every entry in the same shape so it can be scanned. |
| Stop when | Every element of the declared surface is defined and every failure case is listed. Add no tutorial, rationale, or implementation detail. |

## Guidelines

- Declare the surface first: what the spec covers, its version, and what it
  doesn't cover.
- Give every operation or element the same entry shape, for example: summary,
  inputs, output, failures, edge cases, and example.
- For every field, give its name, type, format, whether it is required, its
  default, its allowed values or range, and its units.
- List every failure with the condition that causes it and its exact status,
  code, or message.
- Pin down edge cases explicitly: empty, missing, null, duplicate, too large,
  out of order, concurrent, and retried.
- Include at least one complete, valid example per operation. Examples
  illustrate; the definitions decide.
- If the repository has a machine-readable contract, such as OpenAPI, JSON
  Schema, or protobuf, keep one source of truth: generate the prose from it, or
  point to it instead of restating it.
- Verify the spec against the implementation or the machine-readable contract.
  Report mismatches instead of silently choosing one side.
- Link to the architecture doc or an ADR for reasons; don't explain inline.

## Good examples

**An operation entry** (recipe app):

> **`GET /v1/recipes/{recipeId}/similar`**
>
> Returns up to `limit` recipes most similar to `recipeId`, ordered by `score`
> descending. Ties are ordered by `recipeId` ascending.
>
> | Parameter | In | Type | Required | Default | Constraints |
> | --- | --- | --- | --- | --- | --- |
> | `recipeId` | path | string | yes | | ID of an existing recipe. |
> | `limit` | query | integer | no | `3` | 1 to 10 inclusive. |
>
> **200 OK**: `{"items": [{"recipeId": string, "title": string, "score":
> number}]}`. `score` is from 0.0 to 1.0. A recipe with no ingredients returns
> `{"items": []}`.
>
> | Status | Code | When |
> | --- | --- | --- |
> | 400 | `invalid_limit` | `limit` is not an integer from 1 to 10. |
> | 404 | `recipe_not_found` | No recipe has this `recipeId`. |
> | 503 | `similarity_unavailable` | The similarity index is being rebuilt. The response includes `Retry-After` in seconds. |

It works because every input, output, ordering rule, edge case, and failure is
pinned down.

**A behavioral rule** (banking app):

> Clients MUST send an `Idempotency-Key` header of 1 to 64 printable ASCII
> characters with every `POST /v1/transfers`. A repeated request with the same
> key and the same body returns the original response and moves no money. A
> repeated key with a different body returns `409 idempotency_conflict`. Keys
> expire 24 hours after first use.

It works because it covers the normal case, the repeat, the conflict, and the
time limit, with no reasons attached.

## Bad examples

**A narrative tutorial:**

> To find similar recipes, just call the similar endpoint with your recipe's ID
> and you'll get great suggestions back!

It fails because types, limits, ordering, and failures are left for the reader
to guess.

**Rationale inside the contract:**

> `limit` defaults to 3 because user research showed three suggestions convert
> best, and higher values are slow because of how neighbors are scored.

It fails because a spec states the default and the range. The reasons belong in
the architecture doc or an ADR.

**Vague failures:**

> If something goes wrong, the API returns an error.

It fails because it doesn't say which conditions, which status codes, or which
error codes.

## Template

Use `assets/templates/spec.md`.
