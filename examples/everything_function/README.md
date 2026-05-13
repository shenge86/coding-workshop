# everything_function

A folder full of Python functions. Ten of them. They do ten different things — arithmetic, polynomial root-finding, prime factorization, sentiment analysis, translation, summarization, turning a messy paragraph into an action list, labeling photos, generating recipes from food pictures, reading text out of an image.

Open any of them and you will find roughly the same code:

```python
def ai_something(input):
    prompt = "...some text describing the task, plus a couple of examples..."
    return ask(prompt)   # ← exact same call every time
```

The thing they all share is `ask` — a four-line wrapper around a local AI model. Each function's "logic" lives entirely in the prompt. There is no `if`/`else`. There is no library doing the real work behind the scenes. There is a description of a task, and there is a model predicting what should come next.

If that's all you take from this example, it's the right thing to take.

## The headline

For a wide and growing set of problems, **you can get a usable result by describing the task in plain English and showing a couple of examples** — faster, cheaper, and often *better* than you could by collecting a dataset and training a model specifically for that task. The interesting thing isn't any single demo in this folder. It's that every demo is the same code.

A Python function used to mean "a body of code I wrote." It can also mean "a body of prompt the model continues." Once you see that, you start noticing how much of the work in your life could be described that way.

## What you actually run

Three pieces, all started by the one `docker-compose.yml`:

1. **The `ollama` container** — runs a vision-capable open-weight model (`qwen3.5:9b` by default) locally and exposes an HTTP API. Nothing leaves your machine.
2. **The `web` container** — a small FastAPI service that imports the same `ai_xxx` functions used by the terminal scripts and exposes them on a browser-friendly page at <http://localhost:8082>. This is the one to project for a class.
3. **The scripts in `scripts/`** — small Python programs you run on your host. Each one is a single concept ("AI as a translator", "AI as a prime factorizer") with its own canned examples followed by an interactive REPL. This is the one to read when you want to see exactly what the prompt looks like.

The web UI and the terminal scripts call the *same Python functions*. The web container just wraps them in HTTP. There is no second implementation.

### Prerequisites

Docker Engine + Compose (see [`../../reference/docker/`](../../reference/docker/)). Python 3.10+ on the host if you also want to run the terminal scripts directly (which you should — they're the most instructive view).

### Bring everything up

From this folder:

```bash
docker compose up -d --build
```

That starts `ollama`, kicks off a one-shot `model-puller` container that downloads `qwen3.5:9b` (~6 GB) into a Docker volume, and starts the `web` service. Watch the model download with:

```bash
docker compose logs -f model-puller
```

When you see `Model qwen3.5:9b is ready.`, you're good to go. Subsequent runs reuse the volume — model download happens once.

### Use the web UI

Open <http://localhost:8082> in a browser. Pick a demo from the sidebar (Math / Text / Vision), tweak the inputs, hit Run. Math demos show AI vs. Python side-by-side. Vision demos let you pick a sample image or upload your own.

### Use the terminal scripts

Install the small host-side Python deps once:

```bash
pip install -r requirements.txt
```

Then run any demo:

```bash
cd scripts
python arithmetic.py
python algebra_roots.py
python prime_factorization.py
# ...etc
```

Each script prints a handful of canned examples and then drops into an interactive REPL — type your own inputs at the `>` prompt, type `q` to quit. Vision demos default to images in `sample_images/`; pass `--image PATH` to try your own.

### Pick a different model

Anything in the [Ollama library](https://ollama.com/library) that fits in your RAM will work. The vision demos need a vision-capable model. To swap:

```bash
OLLAMA_MODEL=qwen2.5vl:3b docker compose up -d   # smaller, faster, less accurate
```

The terminal scripts read `OLLAMA_MODEL` from the environment too, so set it in your shell before running them.

### Tear it down

```bash
docker compose down            # stop containers, keep the downloaded model
docker compose down -v         # also delete the model (you'll re-download next time)
```

## The four-ish gears of getting AI to do a thing

When you have a task and want to use AI for it, this is roughly the order to try things in. Start at the top. Stop when it's good enough.

1. **Zero-shot.** Just describe the task. *"Translate this sentence into Japanese."* Often this is all you need, especially with a frontier model. Cost: nothing. Time: one prompt.

2. **Few-shot.** Same prompt, plus a couple of input/output examples. This is what every script in this folder is doing — those little blocks of `Sentence: ... / Sentiment: positive` examples teach the model the output format you want without retraining anything. The GPT-3 paper called this *in-context learning* and made it the headline result, because nobody had quite believed how much of a difference a few examples in the prompt could make. Cost: still nothing. Time: one prompt, maybe slightly longer.

3. **Try a stronger model — or wait for one.** This sounds glib, but it's real: a task that just barely doesn't work on a 7B local model may work on a 32B model, or on a frontier model, or on next year's 7B model. Capability is moving fast enough that "wait six months" is sometimes a legitimate engineering plan. The 7B vision model you're running here would have been an unimaginable result in 2020.

4. **Fine-tune a model.** Take an open-weight model and continue training it on examples specific to your problem. This is real work — you need a dataset, GPU time, and a feedback loop — but the bar is much lower than it used to be. A nice trick: you can often use a frontier model to *generate the first version of your training set*, before you go and collect your own data.

5. **Build the whole pipeline.** Custom data, custom architecture, custom training. This is what you do when none of the above is enough and the problem is worth real money. Most projects never need to come down here.

Most personal projects live happily in step 1 or step 2. Most of the demos in this folder live in step 2. Try step 1 first; reach for step 2 when the answers are inconsistent.

## Local open-weight model vs. paying a frontier lab

We're running a local model in this example. That is a deliberate choice, not the only choice, and it's worth being explicit about the tradeoff.

**Why local / open-weight is the default for this workshop:**

- You are in full control. The model runs on your hardware, your inputs never leave your machine, and the container can run on an airplane.
- Nothing to sign up for, nothing to pay for, nothing to expire.
- You can see *what the model is*. It's a file. You can copy it, version it, swap it out. It's not a magic URL controlled by a company that might change its mind.
- Most importantly: when you can run the thing yourself, you stop being intimidated by it. It becomes another piece of software.

**When a frontier API (Anthropic, OpenAI, Google) is a better fit:**

- You want the strongest possible quality and don't want to wait for open weights to catch up.
- You're building infrastructure and the model is the cheap part of the stack.
- You're prototyping and don't care which model wins — you just want to see whether *any* AI can solve your problem before committing to running one.
- You want a model that is *currently* better than anything you can run at home — frontier models are typically 6–18 months ahead of what fits on a laptop, and that gap matters for hard tasks.

A reasonable workflow: prototype on a frontier API, then swap in a local model once you know the problem is solvable and want to bring the work back in-house. The Python code on your side barely changes — you swap the HTTP endpoint and maybe tweak a prompt.

## What's in `scripts/`

Each file defines one or more functions. Each function is a "smart Python function" backed by the same `ask` call.

| Script | What it does | Hand-written equivalent |
|--------|--------------|-------------------------|
| `arithmetic.py` | Add, subtract, multiply, divide. | `+`, `-`, `*`, `/`. We compare side-by-side. |
| `algebra_roots.py` | Find the real roots of a polynomial. Pretty-prints the polynomial first. | `numpy.roots`. Same — compared side-by-side. |
| `prime_factorization.py` | Factor an integer into its primes. | Trial division. Compared side-by-side. |
| `sentiment.py` | Label a sentence as positive / negative / neutral. | Used to be a research problem. There isn't a clean built-in. |
| `translate.py` | Translate text into any target language. | An API call to Google Translate, basically. |
| `summarize.py` | Shrink a passage to a target word count. | No clean built-in. |
| `action_list.py` | Turn a messy stream-of-consciousness into a bulleted list of actions. | None. This is the kind of thing you can only really do this way. |
| `image_label.py` | "What's in this picture?" | An image classifier. Used to require training one. |
| `recipe_from_food.py` | Picture of food → ingredients and steps. | None. Two tasks combined: identify the dish, then generate a recipe. |
| `ocr.py` | Read printed text out of an image. | Tesseract / ABBYY / paid OCR APIs. |

The first three are the most important. If you watch a 9B local model add two-digit numbers correctly because you wrote `"2 + 3 = 5"` at the top of a prompt — and then watch the exact same code shape factor 360 into primes — you have seen the central trick. Everything else in the folder is the same trick pointed at fancier problems.

## Where this comes from (optional reading)

The "give the model a couple of examples in the prompt" technique is the headline result of [the GPT-3 paper](../../reference/papers/2020_05_28_gpt_3.pdf) (Brown et al., 2020, *Language Models are Few-Shot Learners*). The fact that a vision-language model can answer questions about a picture comes out of [CLIP](../../reference/papers/2021_02_26_CLIP.pdf) (Radford et al., 2021) and what came after it. The reason these models follow your instructions instead of going off and writing related trivia comes from [InstructGPT](../../reference/papers/2022_03_04_instructGPT.pdf) (Ouyang et al., 2022). And if you ever find yourself adding *"let's think step by step"* to a prompt to get a better answer, that's [Chain-of-Thought Prompting](../../reference/papers/2022_01_28_chain_of_thought.pdf) (Wei et al., 2022).

You do not need any of that to run the demos. Read them if you want to know why the technique works at all.

## Caveats worth being honest about

- **The model is wrong sometimes.** For arithmetic with big numbers, for ambiguous prompts, for tasks at the edge of its training. Watch for that — calibration matters more than enthusiasm. Prime factorization is a fun way to break it: small numbers work fine, but it confidently makes up factors for big ones.
- **A 9B model is not a frontier model.** If a demo looks shaky, try the same prompt on a frontier API and see whether it's the technique that's failing or just this particular model. Usually it's the latter.
- **Temperature 0 ≠ deterministic.** Even with `temperature=0`, the same prompt can give slightly different answers across runs, depending on the version of Ollama and the model. Don't be surprised.
- **None of this is engineering best practice.** It's an *example*. Real production AI systems have output validation, retries, structured-output enforcement, monitoring, and so on. Start simple; complicate only when you need to.
