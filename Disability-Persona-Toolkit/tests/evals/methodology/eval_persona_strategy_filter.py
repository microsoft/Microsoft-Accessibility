"""
The principle (see methodology/persona-strategy-filter.md):

    Before reporting a discoverability / visibility concern for a
    persona, check whether the element's position in the interface
    aligns with the persona's documented exploration strategies. If
    the persona's strategies would naturally lead them to discover
    the element, the concern is NOT a real barrier — do not report it.

Two scenarios:

- A "trigger" case where the methodology should fire — the model is
  presented with a draft discoverability finding for a screen reader
  user, but the element is reachable via heading navigation (a
  primary documented strategy). The correct response is to DISMISS
  the finding as a false positive.

- A "no-trigger" case where the principle should NOT fire — the
  draft concern describes an element that none of the persona's
  documented exploration strategies would surface. The correct
  response is to KEEP the concern.

Run with:

    inspect eval tests/evals/methodology/eval_persona_strategy_filter.py \
        --model copilot/gpt-5-mini
"""

from __future__ import annotations

from inspect_ai import Task, task
from inspect_ai.dataset import Sample
from inspect_ai.solver import generate, system_message

from tests.evals import _providers
from tests.evals._context import load_methodology, load_persona_by_alias
from tests.evals._scorers import rubric_scorer

PERSONA_STRATEGY_FILTER = load_methodology("persona-strategy-filter")


def _system_for(persona_alias: str) -> str:
    """Compose a system prompt that pairs the methodology principle
    with the specific persona file whose exploration strategies the
    model must consult.

    The persona file is required context for the principle to be
    applied — step 1 of the methodology is 'identify which exploration
    strategies the active persona uses (from the persona file's
    Exploration Strategies section)'.
    """
    persona = load_persona_by_alias(persona_alias)
    return (
        "You are an accessibility evaluator reviewing draft "
        "discoverability and visibility findings produced by another "
        "evaluator. Apply the following methodology principle exactly:\n\n"
        f"{PERSONA_STRATEGY_FILTER}\n\n"
        "The active persona for this review is provided in full below. "
        "Treat its 'Exploration Strategies' section as the authoritative "
        "list of how this persona discovers elements in an interface. Do "
        "not invent strategies that are not documented, and do not import "
        "strategies from other personas.\n\n"
        "--- PERSONA FILE START ---\n"
        f"{persona}\n"
        "--- PERSONA FILE END ---\n\n"
        "When asked to review a draft discoverability or visibility "
        "concern, decide whether to KEEP it as a finding or DISMISS it as "
        "a false positive. Justify your decision by (a) naming the "
        "specific exploration strategies from the persona file that would "
        "or would not lead the user to the element, and (b) referencing "
        "the persona-strategy-filter principle. Do not flag elements as "
        "hard to discover when a documented strategy would naturally "
        "surface them."
    )


@task
def persona_strategy_filter_triggers() -> Task:
    """The principle SHOULD fire — the draft finding flags an element
    that the persona's documented strategies would naturally surface,
    so it is a false positive and must be DISMISSED.

    Persona: blind screen reader user. Documented strategies include
    heading navigation, landmark navigation, and the elements list —
    so a section sitting under a correctly nested, descriptively
    labelled H2 is in the primary discovery path.
    """
    return Task(
        name="persona_strategy_filter_triggers",
        dataset=[
            Sample(
                input=(
                    "Draft finding to review:\n\n"
                    "  Title: 'Shipping options' section is hard to "
                    "discover for screen reader users.\n"
                    "  Severity: 2 (Moderate).\n"
                    "  Evidence: The 'Shipping options' section appears "
                    "roughly two thirds of the way down a checkout "
                    "page. It is preceded by a 'Cart summary' section "
                    "and followed by a 'Payment' section. Each section "
                    "is introduced by a correctly nested, "
                    "descriptively labelled <h2> element ('Cart "
                    "summary', 'Shipping options', 'Payment'). The "
                    "page also exposes a <main> landmark wrapping all "
                    "three sections, and each section has a <section> "
                    "with an aria-labelledby pointing at its <h2>. "
                    "There are no skip links and no in-page table of "
                    "contents. The screen reader user would have to "
                    "scroll or tab through preceding content to reach "
                    "the section visually.\n"
                    "  Recommendation: Add a skip link or in-page "
                    "table of contents pointing to each section, "
                    "because the section is far from the top of the "
                    "page.\n\n"
                    "Should this finding be KEPT or DISMISSED? Apply "
                    "the persona-strategy-filter principle for the "
                    "active persona."
                ),
            )
        ],
        solver=[
            system_message(_system_for("blind")),
            generate(**_providers.generation_config()),
        ],
        scorer=rubric_scorer(
            [
                {
                    "id": "decides_dismiss",
                    "description": (
                        "Concludes the finding should be DISMISSED as "
                        "a false positive — NOT kept, NOT demoted to a "
                        "manual check, and NOT defended as a real "
                        "discoverability barrier for this persona."
                    ),
                    "weight": 2.0,
                },
                {
                    "id": "names_covering_strategy",
                    "description": (
                        "Names a specific exploration strategy from "
                        "the blind persona file that would surface the "
                        "section — e.g. heading navigation (H key / "
                        "single-letter shortcut), landmark navigation "
                        "(D / R key, <main>), or the elements list "
                        "(JAWS Insert+F3 / NVDA Insert+F7 / VoiceOver "
                        "Rotor). Generic 'screen readers can navigate "
                        "by headings' without tying it to the "
                        "documented strategy does not count."
                    ),
                    "weight": 2.0,
                },
                {
                    "id": "cites_principle",
                    "description": (
                        "References the persona-strategy-filter "
                        "principle by name or paraphrases it "
                        "correctly: if a documented strategy would "
                        "naturally lead the persona to the element, "
                        "the concern is not a real barrier."
                    ),
                    "weight": 1.5,
                },
                {
                    "id": "rejects_skip_link_recommendation",
                    "description": (
                        "Explicitly rejects or removes the skip-link / "
                        "in-page table-of-contents recommendation as "
                        "unjustified for this persona, given heading "
                        "and landmark navigation already provide "
                        "direct jumps."
                    ),
                },
                {
                    "id": "no_sighted_framing",
                    "description": (
                        "Does NOT defend the finding using sighted "
                        "framing such as 'the user would have to "
                        "scroll' or 'the section is far down the "
                        "page' — those are not how this persona "
                        "navigates."
                    ),
                },
            ]
        ),
    )


@task
def persona_strategy_filter_does_not_trigger() -> Task:
    """The principle should NOT fire — none of the persona's
    documented exploration strategies would surface the element, so
    the concern is a real barrier and must be KEPT.

    Persona: low-vision magnifier user. Documented strategies are
    zoomed reading / reflow, magnified-viewport panning (left-to-right
    then down), focus and cursor tracking, high-contrast scanning,
    dual-channel reading, plus baseline visual scanning. An action
    revealed only on hover over an unrelated, far-off-screen icon,
    with no keyboard focus path and no announcement, is missed by
    every one of them.
    """
    return Task(
        name="persona_strategy_filter_does_not_trigger",
        dataset=[
            Sample(
                input=(
                    "Draft finding to review:\n\n"
                    "  Title: 'Delete account' action is not "
                    "discoverable for low-vision magnifier users.\n"
                    "  Severity: 1 (Significant).\n"
                    "  Evidence: On the account settings page, the "
                    "'Delete account' action is implemented as a menu "
                    "item that only appears when the user hovers a "
                    "small gear icon in the top-right corner of the "
                    "page. The gear icon has no visible label, no "
                    "text, and no focus indicator. It is not in the "
                    "tab order. The menu it reveals is rendered as a "
                    "floating <div> with no role, no heading, and no "
                    "landmark. There is no link, button, or heading "
                    "anywhere else on the page that mentions 'Delete "
                    "account'. The persona is using a screen magnifier "
                    "at 6× with the viewport currently centred on the "
                    "left side of the page where the editable profile "
                    "fields are.\n"
                    "  Recommendation: Expose 'Delete account' as a "
                    "real button with a visible label that is "
                    "reachable in the tab order and present in the "
                    "DOM without requiring hover.\n\n"
                    "Should this finding be KEPT or DISMISSED? Apply "
                    "the persona-strategy-filter principle for the "
                    "active persona."
                ),
            )
        ],
        solver=[
            system_message(_system_for("low-vision")),
            generate(**_providers.generation_config()),
        ],
        scorer=rubric_scorer(
            [
                {
                    "id": "decides_keep",
                    "description": (
                        "Concludes the finding should be KEPT as a "
                        "real discoverability barrier for this "
                        "persona — NOT dismissed as a false positive."
                    ),
                    "weight": 2.0,
                },
                {
                    "id": "enumerates_failed_strategies",
                    "description": (
                        "Walks through the low-vision persona's "
                        "documented exploration strategies (e.g. "
                        "magnified-viewport panning, focus and cursor "
                        "tracking, high-contrast scanning, "
                        "dual-channel reading, baseline visual "
                        "scanning) and explains that none of them "
                        "would surface the hover-revealed, "
                        "unlabelled, non-focusable menu item."
                    ),
                    "weight": 2.0,
                },
                {
                    "id": "principle_understood",
                    "description": (
                        "Demonstrates understanding that "
                        "persona-strategy-filter is about suppressing "
                        "concerns covered by a documented strategy — "
                        "NOT about dismissing every discoverability "
                        "finding, and NOT about assuming hidden "
                        "elements are fine because the persona has "
                        "some unrelated strategy."
                    ),
                    "weight": 1.5,
                },
                {
                    "id": "no_invented_strategy",
                    "description": (
                        "Does NOT invent or import a strategy that is "
                        "not in the low-vision persona file (e.g. "
                        "'the user could hover everything to "
                        "discover hidden menus', 'they could use a "
                        "screen reader to find it') to justify "
                        "dismissing the finding."
                    ),
                    "weight": 1.5,
                },
                {
                    "id": "no_unwarranted_dismissal",
                    "description": (
                        "Does NOT dismiss the finding on the grounds "
                        "that the element 'exists in the DOM', is "
                        "'technically reachable', or 'matches a common "
                        "pattern' — the principle is about whether "
                        "the persona's strategies surface it, not "
                        "whether the element is theoretically "
                        "present."
                    ),
                },
            ]
        ),
    )
