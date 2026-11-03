# Persona Strategy Filter

Before reporting a discoverability or visibility concern for a persona, check whether the element's position in the interface aligns with the persona's documented exploration strategies.

## Principle

If the persona's exploration strategies would naturally lead them to discover the element, the concern is not a real barrier — do not report it.

## Examples

- A **low-vision magnifier user** scans left-to-right, then down. Left-aligned elements are in the primary scanning path — do not flag them as hard to discover.
- A **keyboard user** navigates via Tab in rendered order. Elements early in the rendered UI are easily reachable — do not flag them as requiring skip links if focus management already bypasses them.
- A **screen reader user** navigates by headings (71.6% primary method). Content under a well-labeled heading is discoverable — do not flag it as hidden.

## Application

For each potential discoverability or visibility concern:

1. Identify which exploration strategies the active persona uses (from the persona file's "Exploration Strategies" section).
2. Determine whether any of those strategies would naturally lead the user to the element in question.
3. If yes, the element is discoverable for this persona — do not report a concern.
4. If no strategy covers it, report the concern with a rationale explaining why the persona's strategies would miss it.

## Purpose

This filter reduces false positives — findings that sound plausible in the abstract but don't represent real barriers for the specific persona being evaluated. It ensures evaluations are grounded in how users actually navigate, not hypothetical worst cases.
