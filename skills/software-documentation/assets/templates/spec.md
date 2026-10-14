# <Interface> specification

- **Version:** <version>
- **Status:** <draft, stable, or deprecated>

## Contents

- [1. Scope](#1-scope)
- [2. Conventions](#2-conventions)
- [3. <Operation or element>](#3-operation-or-element)
  - [3.1 Inputs](#31-inputs)
  - [3.2 Output](#32-output)
  - [3.3 Failures](#33-failures)
  - [3.4 Edge cases](#34-edge-cases)
  - [3.5 Example](#35-example)

## 1. Scope

- **Covers:** <the operations, formats, or elements this spec defines>.
- **Does not cover:** <related surfaces that are out of scope>.

## 2. Conventions

<Key words such as MUST, SHOULD, and MAY, encodings, units, time formats,
versioning, and the shape of errors.>

## 3. <Operation or element>

<One sentence on what it does.>

### 3.1 Inputs

| Name | Type | Required | Default | Constraints |
| --- | --- | --- | --- | --- |
| `<name>` | <type> | <yes or no> | <default> | <allowed values, range, and units> |

### 3.2 Output

<The exact shape of a successful result, including ordering and empty results.>

### 3.3 Failures

| Condition | Status or code | Caller action |
| --- | --- | --- |
| <When it happens> | `<code>` | <What the caller may do, such as retry after a delay> |

### 3.4 Edge cases

- <Empty, missing, null, duplicate, too large, concurrent, or retried input,
  and the exact behavior.>

### 3.5 Example

```<format>
<A complete, valid example.>
```
