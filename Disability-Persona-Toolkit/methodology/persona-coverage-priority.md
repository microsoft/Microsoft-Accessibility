# Persona Coverage Prioritization

When full persona coverage is not practical — due to time, scope, or resource constraints — use this methodology to prioritize which personas to evaluate first.

## Principle

Persona prioritization is **task-contextual, not static**. The same persona may be high-priority for one UI and irrelevant for another. Prioritize personas whose interaction model diverges most from the baseline user experience **for the specific UI and interactions under evaluation**, with the goal of covering a breadth of persona experiences while avoiding overly redundant considerations.

A persona that uses the same exploration strategies and AT interaction models as the baseline user for a given task adds little evaluation value for that task. A persona whose strategies fundamentally differ from how the baseline user would approach the same task is where barriers are most likely to surface.

## Prioritization Dimensions

Evaluate each available persona against three dimensions for the specific UI under evaluation:

### 1. Task-Contextual Interaction Model Divergence

How much do the persona's exploration strategies and AT interaction models differ from the baseline user's approach **for this specific UI**?

Compare:
- The persona's **exploration strategies** (from their persona file) against the **baseline exploration strategies** (from `_baseline.md`). Which baseline strategies does the persona exclude or replace? Do the replaced strategies matter for this UI?
- The persona's **AT interaction model** against direct manipulation. Does the AT fundamentally change how the user discovers, understands, or operates the UI elements in question?

**High divergence** — the persona's primary interaction model for this UI is fundamentally different from the baseline (e.g., keyboard-only user interacting with a drag-and-drop interface; blind user navigating a data visualization).

**Moderate divergence** — the persona uses mostly the same interaction model but with meaningful differences in specific areas (e.g., low-vision user with a complex form — same interaction model, but magnification changes spatial awareness and label association).

**Low divergence** — the persona's interaction model is essentially the same as the baseline for this UI (e.g., colorblind user on a text-heavy page with no color-coded information; deaf user on a form with no audio content).

### 2. Barrier Frequency for the UI Type

How often does this type of UI **typically** produce barriers for the persona, based on common patterns?

This is a heuristic judgment. Some pairings are known to be high-risk:
- Keyboard-only users + complex interactive widgets (dropdowns, date pickers, drag-and-drop, custom controls)
- Low-vision users + dense layouts, hover-dependent interactions, small touch targets
- Colorblind users + data visualizations, status indicators, form validation using color alone
- Screen reader users + dynamic content, SPAs, custom ARIA widgets, images conveying information
- Deaf users + video/audio content, voice-based interfaces, audio alerts
- Cognitive disability users — `cognitive-memory`, `cognitive-language`, `cognitive-numeracy` — + complex multi-step workflows, time-limited interactions, dense information architecture

### 3. Coverage Breadth

When multiple personas have similar divergence, prefer the combination that covers the widest range of disability categories and AT interaction models.

Covering one motor disability persona, one vision persona, and one perception persona gives broader coverage than covering three vision personas — even if the three vision personas each have high divergence individually.

## How to Apply

For a given UI or interaction under evaluation:

1. **List available personas** relevant to the project scope.
2. **For each persona**, assess task-contextual divergence (high/moderate/low) by examining which of the persona's exploration strategies apply to the UI and how much they differ from baseline.
3. **Order by divergence**: High divergence personas first. Within the same divergence tier, prefer personas with higher barrier frequency for the UI type.
4. **Apply coverage breadth** as a tiebreaker: when two personas have equivalent divergence and barrier frequency, prefer the one that covers a disability category not yet represented.
5. **Evaluate in priority order** until coverage is sufficient or resources are exhausted.

## Examples

### Example: Complex form with validation

| Persona | Divergence | Reasoning |
|---------|-----------|-----------|
| Keyboard-only | **High** | Tab order, focus management, error recovery, and form submission are all keyboard-interaction concerns. Baseline user clicks into fields; this persona must Tab through them. |
| Voice access | **High** | The persona targets controls by visible label. If labels are truncated, mismatched with accessible names, or hidden until hover, the persona cannot reliably activate fields or buttons. |
| Low vision | **Moderate** | Same interaction model (can use mouse), but magnification changes spatial awareness — label/field association, error message proximity, and viewport context are affected. |
| Colorblind | **Moderate** | Same interaction model, but if validation uses color alone (red borders, green success) this persona misses the feedback channel. Divergence depends on the specific form design. |

Priority order: Keyboard-only → Voice access → Low vision → Colorblind

### Example: Dashboard with data visualizations

| Persona | Divergence | Reasoning |
|---------|-----------|-----------|
| Colorblind | **High** | Charts, graphs, and status indicators commonly use color as the primary differentiator. The persona cannot distinguish data series, thresholds, or status without non-color alternatives. |
| Low vision | **High** | Dense data visualizations with small text, thin lines, and low-contrast elements are problematic under magnification and with contrast needs. |
| Voice access | **Moderate** | Interactive chart elements (data points, legend items, filter controls) must have visible labels matching accessible names. Hover-revealed tooltips are inaccessible to voice users. |
| Keyboard-only | **Moderate** | Interactive charts (tooltips on hover, drill-down) may lack keyboard equivalents, but static dashboard viewing has low divergence. |

Priority order: Colorblind → Low vision → Voice access → Keyboard-only

### Example: Video conferencing interface

| Persona | Divergence | Reasoning |
|---------|-----------|-----------|
| Deaf | **High** | Audio is the primary communication channel. Without captions or sign language interpretation, the persona cannot participate in the core function. |
| Hard of hearing | **High** | Partial hearing requires supplementary captions, volume controls, and mono audio fallback. Background noise and crosstalk degrade comprehension without user control over audio levels. |
| Keyboard-only | **High** | Meeting controls (mute, camera, screen share, reactions, chat) must be keyboard-operable. Rich interaction patterns during a live meeting are time-sensitive. |
| Voice access | **Moderate** | Meeting controls must have visible labels matching accessible names. Hover-revealed controls (e.g., participant actions) are inaccessible. However, the core interaction model is label-based activation, which is less divergent than the audio concerns. |
| Low vision | **Moderate** | Video tiles, participant names, and chat may be difficult under magnification, but the core interaction model is similar to baseline. |
| Colorblind | **Low** | Minimal divergence unless the interface uses color-only indicators for mute status, hand raises, or speaker highlighting. |

Priority order: Deaf → Hard of hearing → Keyboard-only → Voice access → Low vision → Colorblind

## Purpose

This methodology ensures that evaluation effort is directed where it will uncover the most significant barriers. It prevents the common failure mode of evaluating personas in a fixed order regardless of context — which wastes effort on low-divergence pairings and may leave high-divergence pairings unexamined when time runs out.
