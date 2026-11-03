# Usability Heuristics with Accessibility Lenses

This file is the entry point for the usability heuristic frameworks used in accessibility evaluation. Each heuristic includes a generic accessibility lens that applies across all personas. Per-persona lens overrides are defined in each persona file's "Heuristic Lens Overrides" section, keeping personas self-contained.

Read the supplementary concerns below, then load only the heuristic file(s) relevant to the evaluation cell you are working on. Listed filenames are relative to this file.

## Supplementary Concerns

These concerns are not mapped to a specific heuristic but should be evaluated across all heuristics:

### Privacy / Discreet

*Incorporates EN 301 549 FPS 4.2.11 (Privacy): "Where ICT provides features that are provided for accessibility, the ICT maintains the privacy of users of these features at the same level as other users."*

Interfaces should support use in social contexts without embarrassment or unwanted disclosure. This applies across all personas and all heuristics. Evaluate whether the interface inadvertently exposes information the user would expect to remain private, including:

- **AT output exposure**: Content spoken aloud by a screen reader in earshot of others, enlarged text visible to bystanders when using screen magnification, and private data exposed through assistive technology output that the user would otherwise expect to remain discreet.
- **Disability status disclosure**: Accessibility features that visually distinguish the user's experience — a separate "accessible version" of a site, an accessibility mode toggle that changes the UI in ways visible to onlookers, or data collection that tracks assistive technology usage. Using accessibility features should not mark the user as different.
- **Accessible version parity**: When a separate accessible version or mode exists, it must provide equivalent content and functionality. If the accessible version is visually distinct (different styling, reduced content), it discloses the user's disability to anyone observing their screen.
- **Volume and audio privacy**: Users who compensate for hearing loss by increasing volume may expose private content to others nearby. Interfaces should support caption alternatives and headphone-compatible audio to mitigate this.
- **Input method privacy**: Voice control users who speak commands aloud ("click My Medical Records") disclose their interaction targets to others in the environment. Screen reader users in public spaces face similar exposure. Interfaces that require interacting with sensitive labels by voice or that announce sensitive content via screen reader without user-controlled verbosity options create privacy risks.

### Bad Prediction

When AI-driven features (autocomplete, smart suggestions, predictive text) predict user intent incorrectly, the cost of recovery is higher for assistive technology users who must sequentially navigate through wrong suggestions. Evaluate whether predictions are dismissible, whether they interfere with the user's assistive technology workflow, and whether the user can efficiently reject and override them.

## Nielsen's 10 Usability Heuristics — Menu

| # | Name | File |
|---|------|------|
| 1 | Visibility of System Status | `h1-visibility.md` |
| 2 | Match Between System and Real World | `h2-match.md` |
| 3 | User Control and Freedom | `h3-control.md` |
| 4 | Consistency and Standards | `h4-consistency.md` |
| 5 | Error Prevention | `h5-error-prevention.md` |
| 6 | Recognition Rather than Recall | `h6-recognition.md` |
| 7 | Flexibility and Efficiency of Use | `h7-flexibility.md` |
| 8 | Aesthetic and Minimalist Design | `h8-minimalist.md` |
| 9 | Help Users Recognize, Diagnose, and Recover from Errors | `h9-errors.md` |
| 10 | Help and Documentation | `h10-help.md` |
