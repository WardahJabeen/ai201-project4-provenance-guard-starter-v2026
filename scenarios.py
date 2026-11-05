"""
What your test runs. ← UNIT 8, MILESTONE 3

Each of your five criteria needs something run against it. A criterion about
false positives needs your own writing. One about label coverage needs inputs
across the score range. One about the appeal path needs a real content_id.

Working that out is Milestone 3's first step, and this file is where you write
it down. `run_eval.py` runs everything here three times.

Two are filled in as examples. Replace them with what your criteria actually
need — these are a shape, not a set.

A scenario carries **either** of these:

    "texts"   a list of strings. Each is sent as {"text": ..., "creator_id": ...}
              with a creator_id made up for you. Use this for most criteria.

    "bodies"  a list of whole request bodies, sent exactly as written. Use this
              when the malformed request IS the point — empty text, no `text`
              field at all, something enormous. A bad-input criterion needs it,
              because you cannot express "the field is missing" as a string.
"""

# ── Criterion 1 needs MY OWN writing ─────────────────────────────────────────
# Ten pieces I actually wrote, at least three of them plain (short sentences,
# everyday words). The first five double as the "clearly human" group for
# criterion 2.
MY_WRITING = [
    # 1–5: my college essay on dreams and aspirations, one chunk each.
    "Technology has always intrigued me, be it a television remote, a cell phone and function generators. This fascination with technology also extended to computers. I had never dared to open a computer up, but when my own computer broke down, I was presented the perfect opportunity to see its inner workings.",
    "I excitedly searched the house for a screwdriver and tried to open the computer case. After half an hour of struggling, I was finally successful, and what lay before me was the most intriguing sight ten year old me had ever seen, but the problem remained: how would I get my computer to work?",
    "After tinkering and some simple trial and error, I found that one of the power connectors inside the computer had come loose. By reattaching the power connector I had fixed my first computer. Over the coming years I would fix many computers, each one with more complicated problems.",
    "What started as a love for hardware would extend to an appreciation of software in the following years. This passion for computers  was further cultivated by my computer teachers, international competitions like Thinkquest hosted by Oracle, and programming classes.",
    "In an effort to translate my passion for technology into a career, I’ve set my mind on becoming an  electrical or computer engineer, and eventually starting my own tech startup which I will hopefully be able to make something bigger over time.",
    # 6–10: my own messages from working on this project, typed casually.
    # 6–9 are the plain ones: short, everyday words, no polish.
    "where did we get the idea to use even sentences for AI label? I feel like the main thing that tells its AI is that its very abrupt as if its giving order, especially instruction, they lack warmness",
    "also for readme not sure what you mean by you vs I? is that what AI uses? I believe for instructions humans use you and I but AI just commands it without you/I",
    "Could you please replace this one with something longer?",
    "Could you take out some of my text from the chat history (not the direct instruction part) but perhaps even this and fill the rest of the pieces?",
    "One of the recent codepath assignment was pretty interesting. We basically had to write a webserver to detect whether the writing was from ai or human. the core idea was to detect people used ai but more so that we don't want honest people to be flagged as ai as that can be heavily discouraging.",
]

# ── Criterion 2: five clearly AI-generated texts ─────────────────────────────
# Written by an AI assistant for this test. The first is detector.py's own
# sample; the last is the overly warm chatbot tone I noticed in Milestone 4.
CLEAR_AI = [
    "The implementation of the proposed framework requires careful consideration of several key factors. First, it is important to note that the system must be able to handle a wide variety of different inputs. Additionally, the overall performance of the solution depends on a number of important variables.",
    "Effective time management is essential for achieving success in both personal and professional contexts. By prioritizing tasks, setting clear goals, and minimizing distractions, individuals can significantly enhance their productivity. Furthermore, adopting consistent routines can help reduce stress and improve overall well-being.",
    "Climate change represents one of the most significant challenges facing humanity today. Rising global temperatures have led to more frequent extreme weather events, which pose serious risks to communities and ecosystems. It is therefore crucial that governments, businesses, and individuals work together to implement sustainable solutions.",
    "Artificial intelligence has the potential to transform a wide range of industries. From healthcare to finance, AI-powered tools can streamline processes, improve decision-making, and unlock new opportunities for innovation. However, it is important to consider the ethical implications of these technologies to ensure they are used responsibly.",
    "Great question! Learning a new language can be a rewarding experience. Here are a few tips to help you get started: practice consistently, immerse yourself in the language through music and movies, and don't be afraid to make mistakes. Remember, every step forward is progress, and with patience and dedication, you'll achieve your goals!",
]

SCENARIOS = [
    {
        "name": "my own writing",
        "criterion": 1,
        "texts": MY_WRITING,
    },
    {
        "name": "clear AI",
        "criterion": 2,
        "texts": CLEAR_AI,
    },
    {
        "name": "clear human",
        "criterion": 2,
        "texts": MY_WRITING[:5],
    },
    {
        "name": "label coverage",
        "criterion": 3,
        # Inputs from earlier milestones that landed in each band:
        # detector sample (AI), my AI instructions sample (human, wrongly),
        # my own question and the in-between paragraph.
        "texts": [
            CLEAR_AI[0],
            "Pick one public community with lots of text and real variation in quality. Sports forums, music discussion boards, film communities, and gaming subreddits all work. You need to be able to collect 200 public posts from it. "
            "Two rules. Public only — nothing behind a login you had to be invited to. And avoid communities built around one show or one release, since spoilers make your examples unreadable for anyone who isn't caught up.",
            "It seems like I have uncommited files. I can't remember if its the latest working version that I forgot to commit or if its something buggy. Can you give me a brief summary of files and the changes that hasnt been commited in simple terms?",
            "Being wrongly accused of using AI can really hurt a writer, while a bit of AI text slipping through costs the site much less. So I allow at most 1 mistake in 10. I'm including plain writing on purpose, because that's the kind my first signal struggles with, and I'd rather see the problem than hide it behind my most polished work.",
        ],
    },
    # Criterion 4 (appeals) can't run from here: it needs a submission, then an
    # appeal against the content_id that came back. eval_appeals.py does that.
    {
        "name": "bad input",
        "criterion": 5,
        # The five bad requests named in criteria.md. Each has its own
        # creator_id so the rate limiter doesn't answer before my route does.
        "bodies": [
            {"creator_id": "eval_bad_missing"},
            {"text": "", "creator_id": "eval_bad_empty"},
            {"text": "Too short to score.", "creator_id": "eval_bad_short"},
            {"text": "word " * 2001, "creator_id": "eval_bad_long"},
            {"text": None, "creator_id": "eval_bad_null"},
        ],
    },
]


def validate() -> list[str]:
    """
    Complain about anything malformed, before a long run rather than during.

    A "bodies" scenario is deliberately exempt from the empty check — an empty
    string is the whole point of a bad-input case, and refusing to run one
    would make that criterion untestable.
    """
    problems = []
    for i, scenario in enumerate(SCENARIOS, 1):
        if not scenario.get("name"):
            problems.append(f"scenario {i} has no name")

        texts = scenario.get("texts")
        bodies = scenario.get("bodies")

        if texts and bodies:
            problems.append(
                f"scenario {i} ('{scenario.get('name')}') has both texts and "
                f"bodies — pick one"
            )
            continue

        if bodies:
            for j, body in enumerate(bodies, 1):
                if not isinstance(body, dict):
                    problems.append(
                        f"scenario {i}, body {j} is not a dict — bodies are whole "
                        f"request bodies, like {{'text': '', 'creator_id': 'x'}}"
                    )
            continue

        if not texts:
            problems.append(f"scenario {i} has no texts and no bodies")
            continue

        for j, text in enumerate(texts, 1):
            if not str(text).strip():
                problems.append(
                    f"scenario {i}, text {j} is empty — if an empty submission is what "
                    f"you're testing, use 'bodies' instead of 'texts'"
                )
            elif str(text).startswith("REPLACE ME"):
                problems.append(
                    f"scenario {i} ('{scenario.get('name')}'), text {j} is still "
                    f"the placeholder"
                )
    return problems
