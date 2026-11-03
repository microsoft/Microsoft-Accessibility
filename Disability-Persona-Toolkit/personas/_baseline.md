---
type: baseline
title: Universal baseline strategies, variants, and learning considerations
description: >
  The universal foundation that all users share — sighted, hearing, full motor control,
  typical cognition. Disability-specific personas inherit from this baseline and override
  or extend it. The baseline is NOT an evaluable persona on its own.
---

# Universal Baseline

This file defines the shared exploration strategies, user variants, and learning considerations that apply to all users regardless of disability. Each elaborated persona file includes applicable baseline content inline (self-contained), excluding strategies that don't apply to that persona.

> Use personas to evaluate interface barriers, not to classify real people. Do not infer
> disability, diagnosis, capability, or accommodation from behavior, zoom level, preferences, or
> assistive-technology use. See
> [`methodology/responsible-persona-use.md`](../methodology/responsible-persona-use.md).

## Exploration Strategies

### Visual scanning and layout comprehension

The user scans the page visually to understand its layout: header, navigation, main content, sidebar, footer. They identify interactive elements by their visual affordances — buttons look clickable, links look tappable, text fields look fillable. Visual hierarchy (headings, spacing, colour, size) guides their attention to primary content and actions.

**AT Mechanisms**: Visual perception
**Device context**: All

**UI Requirements**: Clear visual hierarchy through headings, spacing, and grouping. Interactive elements must look interactive (visible borders, underlines, or other affordances). Primary actions should be visually prominent.

### Mouse / pointer interaction

The user moves a mouse, trackpad, or touch pointer to interact with elements. They click buttons, select text, drag items, hover for tooltips, and right-click for context menus. Hover states provide feedback about what is interactive.

**AT Mechanisms**: Mouse, Trackpad, Touchscreen
**Device context**: Desktop

**UI Requirements**: Interactive elements are easy to activate with the intended pointer action and are far enough apart that users do not accidentally activate adjacent controls. Hover states should indicate interactivity. Drag-and-drop should have clear affordances.

### Reading and scrolling

The user reads text content sequentially or by scanning headings. They scroll vertically (and sometimes horizontally) to access content beyond the viewport. They expect content to flow logically top-to-bottom, left-to-right (in LTR languages).

**AT Mechanisms**: Visual reading, Mouse wheel / scroll gesture
**Device context**: All

**UI Requirements**: Text must be readable: sufficient contrast, reasonable font size, adequate line spacing. Content should not require horizontal scrolling at standard viewport widths. Long pages should provide navigation aids (table of contents, back-to-top).

### Form interaction

The user fills out forms by clicking into fields, typing, selecting from dropdowns, checking boxes, and submitting. They expect clear labels, helpful placeholder text (that doesn't replace labels), and immediate feedback on errors.

**AT Mechanisms**: Keyboard (typing), Mouse (clicking fields), Visual reading (labels)
**Device context**: All

**UI Requirements**: Every form field must have a visible label. Required fields must be clearly indicated. Error messages must be specific, adjacent to the field, and visible without scrolling. Successful submission must be clearly confirmed.

### Navigation and wayfinding

The user navigates between pages/views using menus, breadcrumbs, links, and browser back/forward. They build a mental model of the application's structure. They expect to know where they are, where they can go, and how to get back.

**AT Mechanisms**: Visual scanning, Mouse clicking, Browser controls
**Device context**: All

**UI Requirements**: Consistent navigation across pages. Current location clearly indicated (active nav item, breadcrumbs). Important actions reachable from any page. Browser back button should work predictably.

### Touch / pointer interaction

The user taps, swipes, pinch-zooms, and long-presses on a touchscreen to interact with elements. There is no hover state — the user cannot preview interactivity before activating. Touch targets must be large enough to hit accurately. Gestures (swipe, pull-to-refresh) must be discoverable and have single-pointer alternatives.

**AT Mechanisms**: Touchscreen tap, Swipe gestures, Pinch-zoom
**Device context**: Mobile

**UI Requirements**: Touch targets are easy to activate without accidentally activating adjacent controls — small or tightly packed targets force users to retry or hit the wrong control. No reliance on hover for essential information. Custom gestures must have single-pointer alternatives. Drag-and-drop must have tap-based alternatives. No accidental activation from scroll gestures.

## User Variants

### New / infrequent user

Encountering the interface for the first time or after a long gap. Relies on visual affordances, labels, and progressive disclosure to learn the interface. Cannot recall shortcuts or hidden features.

**Primary AT**: None
**Device context**: All
**Preferred navigation**: Visual scanning and layout comprehension, Navigation and wayfinding, Form interaction

**Expectations**:
- Interface is learnable without documentation
- Primary actions are visually obvious
- Error messages guide toward resolution
- Navigation structure is understandable

### Expert / frequent user

Uses the interface regularly and has built a mental model. Relies on consistency, shortcuts, and efficient workflows. Notices and is disrupted by changes to established patterns.

**Primary AT**: None
**Device context**: All
**Preferred navigation**: Mouse / pointer interaction, Navigation and wayfinding

**Expectations**:
- Keyboard shortcuts for common tasks
- Consistent layout across sessions and pages
- Efficient paths to frequently used features
- Changes to familiar workflows are clearly communicated

## Learning Considerations

- **First visit**: The user approaches the interface with expectations set by common platform conventions (web, desktop, mobile). Standard UI patterns (hamburger menu, search icon, tabs, modals) are recognized immediately. Non-standard patterns require learning.

- **Mental models**: Users build a model of how the interface works based on early interactions. If the model is violated later (e.g., a button that sometimes navigates and sometimes submits), trust erodes and the user becomes cautious and slower.

- **Error recovery**: All users occasionally make mistakes. The interface should make errors recoverable (undo, confirmation dialogs, clear error messages) rather than punishing. Irreversible actions without confirmation are universally problematic.

- **Cognitive load**: Every interface competes for the user's attention. Cluttered layouts, excessive options, and unclear hierarchy increase cognitive load for everyone, not just users with cognitive disabilities.

## Baseline Exclusions by Persona

When a disability persona inherits the baseline, it excludes strategies that don't apply:

| Persona | Excluded Baseline Strategies |
|---------|------------------------------|
| 4.2.1 (Blind) | Visual scanning and layout comprehension, Mouse / pointer interaction |
| 4.2.7 (Keyboard-only) | Mouse / pointer interaction, Touch / pointer interaction |
| 4.2.7b (Voice-access) | Mouse / pointer interaction, Touch / pointer interaction, Form interaction |
| 4.2.8 (Limited-reach) | *(no exclusions — pointer-modality persona uses all baseline strategies)* |
| 4.2.3 (Colour-blind) | *(no exclusions — uses all baseline strategies)* |
| 4.2.2 (Low-vision) | *(no exclusions — uses all baseline strategies)* |
| 4.2.6 (Without speech) | *(no exclusions — uses all baseline strategies)* |
