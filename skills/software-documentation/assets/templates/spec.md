# <Interface> specification

- **Version:** <version>
- **Status:** <draft, stable, or deprecated>

## Scope

- **Covers:** <the operations, formats, or elements this spec defines>.
- **Does not cover:** <related surfaces that are out of scope>.

## Conventions

<Key words such as MUST, SHOULD, and MAY, encodings, units, time formats,
versioning, and the shape of errors.>

## <Operation or element>

<One sentence on what it does.>

### Inputs

| Name | Type | Required | Default | Constraints |
| --- | --- | --- | --- | --- |
| `<name>` | <type> | <yes or no> | <default> | <allowed values, range, and units> |

### Output

<The exact shape of a successful result, including ordering and empty results.>

### Failures

| Condition | Status or code | Caller action |
| --- | --- | --- |
| <When it happens> | `<code>` | <What the caller may do, such as retry after a delay> |

### Edge cases

- <Empty, missing, null, duplicate, too large, concurrent, or retried input,
  and the exact behavior.>

### Example

```<format>
<A complete, valid example.>
```
