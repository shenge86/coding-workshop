# Papers

A curated reading list. The goal isn't to make you a researcher — it's to give you a *feel* for how the tools you're using actually came to exist, why the last few years surprised even the people building them, and why the same trick keeps eating new domains.

You can skip this section entirely. Nothing else in the workshop depends on it.

> Each PDF is prefixed with its publication date (`YYYY_MM_DD_…`) so the directory listing sorts chronologically. The sections below organize the same papers by *track* (language, images, games, the physical world) — but if you'd rather walk through them in pure release order, just sort the folder by name.

## The pattern, in one sentence

Take a general-purpose neural network, give it a stupidly simple objective (*predict the next word*, *win the game*, *find the shape of the protein*), and pour in absurd amounts of compute and data. Out the other side comes a system that solves a problem we used to think required something distinctly human. The papers below are the same trick, applied to wildly different problems, over the course of about a decade.

If you read these in order, three things should land:

1. **The leap was not one breakthrough.** It was the same handful of ideas, scaled up and pointed at new targets. You're not watching ten different revolutions — you're watching one revolution arrive in ten different rooms.
2. **The "AI does that now?" era is shockingly recent.** The transformer architecture is 2017. AlphaGo is 2016. The model most people would say passes an informal Turing test (GPT-4) is 2023. Protein structure prediction stopped being an unsolved problem in 2021. Drones started beating human world champions at racing in 2023. End-to-end, the surprising stuff fits inside a single decade.
3. **It is not just about chatbots.** Text, images, games, robotics, biology — the *same family of techniques* is making progress in all of them, often by the same labs. If you're trying to predict what gets disrupted next, that's the signal worth tracking.

By the end you should have the vocabulary to read AI announcements skeptically, and a working theory of where the field is going next.

## The unifying recipe

Across every paper here, four ingredients show up over and over. If you only remember one thing, remember this list — it's how to spot a paper that's part of the trajectory versus a paper that isn't.

1. **A simple, scalable objective.** No hand-designed rules. "Predict what comes next," "win the game," "match the experimental data." The training signal is something a computer can grade automatically, which means it can be applied at enormous scale.
2. **A general-purpose architecture.** Mostly neural networks, and increasingly the *same* neural network blueprint (the transformer) across very different problems. There's no separate "language brain" and "vision brain" — there's one machine that learns whatever you feed it.
3. **Self-generated or web-scale data.** Either the model learns from a huge slice of the internet, or — even better — it generates its own training data by playing against itself or simulating the world.
4. **Compute, scaled aggressively.** More parameters, more data, more chips, more electricity. Capabilities improve in a way that's now predictable in advance (this is what "scaling laws" means).

When you see a result that combines those four, that's the trajectory. When you see a result that brags about clever hand-designed features and works on a small dataset, that's a different (and shrinking) part of the field.

## Track 1 — Language

The trunk of the tree. Everything modern starts here, even results that aren't about text.

**[Attention Is All You Need](2017_06_12_attention_is_all_you_need.pdf)** — *Vaswani et al., Google, 2017.* The transformer paper. Before this, language models read text one word at a time, like a person reading left to right. The transformer reads everything at once and learns which words should "pay attention" to which other words. That's the whole architectural change. Every chatbot you've used is downstream of this paper. Stare at Figure 1 for a minute, skim the intro, skip the math.

**[GPT-1: Improving Language Understanding by Generative Pre-Training](2018_06_11_gpt_1.pdf)** — *Radford et al., OpenAI, 2018.* The recipe: take a transformer, train it on a huge pile of text to predict the next word, then lightly fine-tune it for whatever task you actually care about. This is the template everyone copies for the next five years. About 117 million parameters — small enough to run on a single beefy GPU today.

**[GPT-2: Language Models are Unsupervised Multitask Learners](2019_02_14_gpt_2.pdf)** — *Radford et al., OpenAI, 2019.* Same recipe, ten times bigger, ten times more text. It can now write coherent paragraphs. OpenAI initially refused to release the largest version because they thought it was too dangerous — the first time anyone seriously argued that a language model itself could be a hazard.

**[GPT-3: Language Models are Few-Shot Learners](2020_05_28_gpt_3.pdf)** — *Brown et al., OpenAI, 2020.* Same recipe, a hundred times bigger again. Something unexpected happens: you stop needing to fine-tune the model for new tasks. Describe the task in the prompt, give it a couple of examples, and it figures out what you want. The first sign that scale wasn't just buying better autocomplete — it was buying *generality*.

**[Scaling Laws for Neural Language Models](2020_01_23_scaling_laws.pdf)** — *Kaplan et al., OpenAI, 2020.* The paper that turned "make it bigger" from a hunch into a forecast. Performance improves with model size, data, and compute in smooth, predictable curves. This is why labs felt comfortable spending hundreds of millions of dollars on a single training run: the result was no longer a gamble.

**[Training Compute-Optimal Large Language Models ("Chinchilla")](2022_03_29_chinchilla.pdf)** — *Hoffmann et al., DeepMind, 2022.* A correction to the earlier scaling laws. Everyone had been making models that were *too big and too undertrained*. Match data to model size properly and you get more performance for the same money. The reason modern open models punch above their weight is largely this paper.

**[Training Language Models to Follow Instructions ("InstructGPT")](2022_03_04_instructGPT.pdf)** — *Ouyang et al., OpenAI, 2022.* The missing piece between GPT-3 and ChatGPT. The base model from the GPT-3 paper is a brilliant-but-feral autocomplete — give it "Q: what's the capital of France?" and it might respond with a list of more trivia questions instead of an answer. InstructGPT introduces *reinforcement learning from human feedback* (RLHF): people rank model outputs, and the model learns to prefer the kind of response humans want. This is the paper that made AI feel like a product instead of a research demo.

**[Chain-of-Thought Prompting Elicits Reasoning](2022_01_28_chain_of_thought.pdf)** — *Wei et al., Google, 2022.* A tiny paper with outsized consequences. Just add "let's think step by step" to a prompt and large models suddenly become much better at math and logic, because they show their work. This is the seed of the current reasoning-model era (the o1 / o3 / Claude-with-extended-thinking line) — those systems are, roughly, "what if we trained the model to do this on every problem, all the time?"

**[GPT-4 Technical Report](2023_03_15_gpt_4_technical_report.pdf)** and **[GPT-4](2023_03_15_gpt_4.pdf)** — *OpenAI, 2023.* The model most people would agree passes an informal Turing test. Performs at or near human level on a wide range of academic and professional exams. Accepts images as input — the moment language models became *multimodal*. The report is striking for what it leaves out: no model size, no architecture details, no training data details. The opacity is part of the story — frontier AI has become a commercial product, not an open science project. Read the "Predictable Scaling" section (they forecast GPT-4's performance from much smaller test runs — scaling laws, in action) and the "Limitations" section.

## Track 2 — Images

The same machinery, pointed at pixels. Watch the architecture diverge from the text track around 2020, then converge again around 2023.

**[Learning Transferable Visual Models from Natural Language Supervision ("CLIP")](2021_02_26_CLIP.pdf)** — *Radford et al., OpenAI, 2021.* The bridge between language and vision. CLIP learns to put images and captions into the same conceptual space, so "a photo of a golden retriever" and the actual photo end up nearby. Suddenly you can search images by description, classify pictures you've never trained on, and — crucially — *condition image generators on text*. Almost every text-to-image system since runs on top of this idea.

**[DALL·E 1: Zero-Shot Text-to-Image Generation](2021_02_24_dalle_1.pdf)** — *Ramesh et al., OpenAI, 2021.* "What if we did GPT, but for images?" Chop images into a grid of tokens (like words), and train a transformer to predict the next image-token given a caption. Results were rough but stunning in 2021 — the first time a single model could draw an arbitrary thing you described in plain English.

**[Denoising Diffusion Probabilistic Models](2020_06_19_diffusion_models.pdf)** — *Ho et al., Berkeley, 2020.* The other paradigm for generating images. Instead of predicting pixels one at a time, start with pure noise and gradually denoise it into a picture. Counterintuitive, mathematically elegant, and — it turns out — much better at producing photorealistic images than the autoregressive approach. Every modern image generator (Stable Diffusion, Midjourney, DALL·E 2 and 3) descends from this paper.

**[High-Resolution Image Synthesis with Latent Diffusion Models](2021_12_20_latent_diffusion.pdf)** — *Rombach et al., 2022.* Also known as the Stable Diffusion paper. The trick: instead of denoising pixels directly (slow, expensive), compress the image into a much smaller "latent" representation first and denoise *that*. The result is a diffusion model you can actually run on a consumer GPU. This is the paper that made image generation a thing normal people could do at home.

**[DALL·E 2: Hierarchical Text-Conditional Image Generation with CLIP Latents](2022_04_13_dalle_2.pdf)** — *Ramesh et al., OpenAI, 2022.* Combines CLIP with diffusion. Quality jumps from "interesting curiosity" to "could plausibly be a commercial product." Note the architectural divergence from the text track: image generation has now broken away from the pure transformer recipe.

**[DALL·E 3](2023_09_20_dalle_3.pdf)** — *OpenAI, 2023.* Less an architectural leap than a usability one. The headline: it actually follows your prompt. Earlier image models ignored half of what you asked for; DALL·E 3 leans on a GPT-style model to interpret what you wrote, then generates accordingly. The end of the "trending on artstation, 8k, hyperreal" era of prompt engineering. By 2023 the language and image tracks have converged again, with language models in the driver's seat.

## Track 3 — Games and self-play

This track predates the modern language work and quietly establishes the most important pattern in the whole list: *the model can supervise itself.*

**[Mastering the Game of Go with Deep Neural Networks and Tree Search ("AlphaGo")](2016_01_28_Mastering_the_game_of_Go_with_deep_neural_networks.pdf)** — *Silver et al., DeepMind, 2016.* Go was the canonical problem that brute-force search couldn't solve — too many positions, too few patterns a programmer could write down. AlphaGo combined deep neural networks (for intuition about which moves look good) with tree search (for verifying) and beat the world champion. Until this paper, "AI plays Go at superhuman level" was a thing experts said was decades away.

**[Mastering Chess and Shogi by Self-Play ("AlphaZero")](2017_12_05_mastering_chess_and_shogi.pdf)** — *Silver et al., DeepMind, 2017.* The deeper result. AlphaGo learned from a database of human games. AlphaZero starts from random weights, plays itself for a few hours, and reaches superhuman play in chess, shogi, and Go using the *same algorithm and architecture* for all three games. Two things to take from this paper: (1) the same general technique handles multiple distinct problems, and (2) human data is a *crutch*, not a requirement, when the system can generate its own. That second insight is now reshaping how the language models in Track 1 get trained for reasoning.

## Track 4 — The physical and natural world

Where the pattern is now arriving. These three results are less famous than ChatGPT, and arguably more important.

**[Champion-level Drone Racing using Deep Reinforcement Learning](2023_08_30_superhuman_drone_racing.pdf)** — *Kaufmann et al., UZH, Nature 2023.* An autonomous drone (the system is called Swift) that beats human world champions in head-to-head racing through a physical course at over 50 mph. The interesting bits: it learns in simulation, transfers to the real world, and runs entirely onboard the drone — no remote supercomputer in the loop. This is what it looks like when the recipe leaves the data center and enters a body. Robotics has been "five years away" for forty years; results like this are the reason that's starting to change.

**[Highly Accurate Protein Structure Prediction with AlphaFold ("AlphaFold 1")](2020_01_15_alphafold.pdf)** — *Senior et al., DeepMind, 2020.* Proteins are strings of amino acids that fold into 3D shapes, and the shape determines what the protein does. Predicting that shape from the sequence was one of biology's grand challenge problems for fifty years. AlphaFold 1 was the system that won the field's blind benchmark (CASP13) in a way nobody had before. Set the stage for the result that actually closed the problem out.

**[Highly Accurate Protein Structure Prediction with AlphaFold ("AlphaFold 2")](2021_07_15_alphafold2.pdf)** — *Jumper et al., DeepMind, Nature 2021.* The structure-prediction problem, effectively solved. Predictions at accuracies competitive with experimental measurements that take months in a lab. DeepMind released the structures of essentially every known protein for free, an act that probably accelerated biology by years. If you want a concrete example of "AI did something that mattered outside computer science," this is the one to point at.

**[Accurate Structure Prediction of Biomolecular Interactions ("AlphaFold 3")](2024_05_08_alphafold3.pdf)** — *Abramson et al., DeepMind, Nature 2024.* AlphaFold 2 handled proteins in isolation. AlphaFold 3 handles proteins *interacting with* DNA, RNA, drug molecules, ions — the actual machinery of a cell. Architecturally, it borrows from the image-generation track (it uses diffusion). The convergence is the point: techniques developed for cat pictures are now used to design medicines.

## What it all means

Step back from the individual papers and what you have is something like this:

A general-purpose technique — neural networks trained at scale on simple objectives — keeps walking into fields that previously demanded specialized expertise, and within a few years it's competitive with or better than the specialists. Language. Vision. Games requiring intuition. Real-time control of physical machines. Predicting how molecules behave. Each of these used to be its own subfield with its own community and its own decade-long roadmap. Now they share an underlying method, and progress in one often transfers to the others.

The features that show up everywhere are the four from the recipe section: simple objective, general architecture, scalable data, lots of compute. There is no obvious wall yet. Compute keeps getting cheaper, models keep getting better in ways that scaling laws keep predicting, and the set of "problems we used to think needed a human specialist" keeps shrinking.

For most people, the practical implications are roughly:

- **Anything that can be framed as "predict the next thing" is fair game** — and that turns out to include most knowledge work, a lot of creative work, and an increasing slice of physical work too.
- **The bottleneck is shifting from "can a machine do this?" to "have we pointed the machine at it yet?"** Most of the value over the next decade will come from people who notice an unaddressed problem, gather the right data, and apply the recipe — not from new architectures.
- **The trajectory is jagged, not smooth.** Capabilities arrive in lumps. Whole categories of work look untouched until they're suddenly not. Plan for surprise.
- **Where this most likely goes next:** systems that take actions in the world (agents, robots), systems that do real scientific discovery (the AlphaFold pattern applied to chemistry, materials, medicine), and reasoning systems that can chain together long thought processes before answering. All three are already in flight.

If you finish this list and one feeling sticks, it should be this: *the surprising stuff isn't done arriving.*

## How to read a paper without a PhD

- Read the abstract first. If it doesn't grab you, skip it.
- Look at the figures. They usually carry most of the story.
- Read the introduction and the conclusion. Skip methods and experiments unless you care about the details.
- Paste sections into a chatbot and ask "explain this like I'm not a researcher." It will do a remarkably good job — which is itself part of the point.
- Don't try to *implement* anything from a paper unless that's your project.
