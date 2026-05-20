# AI Workshop

A hands-on work shop where we will use technology to solve actual problems in your own life.

Today's technology is more capable than ever, and you might be surprised just how easy it is to control with the right techniques and mindset. Yet somehow the supposed miracles of technological development have yet to impact our lives in a positive way. Rather than serving us, we often find the opposite -- many of most commercially successful AI applications _feed_ on our attention, often at the cost of our wellbeing. That's not because AI is evil, just the unfortunate alignment of incentives that many of the top tech talent also wants to make money. Rather than unknowingly selling your attention and data, you can take control and make your technology work for you.

This workshop

This course will focus around a personal project: something that would help you in your life or just something you think is cool. We're going to use te

This is not a programming course, though programming is supplemental. It's not a test or credential. You showed up because you're curious and motivated, and our job is to help you turn that into

---

## Who's running this

Ryan Franz and Shen Ge. Friends and engineers with backgrounds in physics, programming, and aerospace. We have decades of combined experience getting hard things to work in the real world, including putting 2 NOVA-C landers on the Moon with the IM-1 and IM-2 missions. We know how to make technology work and we can help you get your technology to work. We'll put you in the driver seat of your own technology. How can we promise that? We're not the teachers, we're the guides. AI is the teacher. The skill is having a vision, knowing what's reasonable, and knowing where to look when things go wrong.

---

## The bet behind this class

There is a widening gap between what technology can do and what most people are *using* technology to do.

In the last few years, a new generation of AI tools has made it possible for a single motivated person — without a software background — to direct a computer to do things that, until very recently, required teams of engineers. The technology is here. What's missing, for most people, is the awareness that they can pick it up and use it themselves.

That is what this class is about: closing that gap, one person at a time.

---

## What you'll actually do

There is one organizing idea: **your personal project**.

Somewhere in your life, there's friction. A repetitive task you do by hand. Not being able to find things because you organize them into random piles in your attic. A small business workflow that should take 5 minutes and takes 45. Something you've been meaning to figure out for years but never had the time. 

It's never been easier to address these frictions than the present. It doesn't have to be today, but I want you thinking: if you were Iron Man and you could just snap your fingers and make your laptop, cellphone, smart devices do anything you wanted, what would you do with that power? It's not just "hypothetically possible" with AI. AI _is_ that power, and it's probably already in your pocket. It's my job to guide and motivate you into realizing what you can do with that.


See [`personal-project.md`](personal-project.md) for more on what a project can look like and how loose the requirements are. (Spoiler: very loose.)

---

## What this class is *not*

- **Not a SaaS demo.** We are not going to teach you how to pay company X to do thing Y. The whole point is to put *you* in control.
- **Not a graded class.** No tests, no homework, no minimum project complexity, no wrong answers, you can't mess up. Being present is the bar.
- **Not a credential.** There is no credential associated with taking this class. The reward is understanding how to use technology. Although if you _want_ I'll invent a digital token that we can agree represents a credential, and I'll try to convince why that's more authentic and useful than any other artifact I could hand you.
- **Not a promise that everything is easy.** Some things will be frustrating. The two of us are here to get you unstuck when you are.

---

## Our biases (so they're not surprises)

- **Free and open source by default.** Open-weight models, self-hostable tools, standard formats. We will not steer you into a walled garden if we can help it.
- **Local-first when it's reasonable.** Running things on your own machine is often simpler, cheaper, and more private than people assume. Cloud compute has genuine uses too but you should have an idea of what's reasonable.
- **Honest about limits.** AI is powerful and AI is fallible. We'll show you both. Calibration matters more than hype.

---

## Sessions

We're starting with one class. If it feels valuable to people, it continues.

- [`sessions/01-orientation.md`](sessions/01-orientation.md) — what to expect at the first session

---

## Repository layout

```
.
├── README.md              ← you are here
├── personal-project.md    ← what a personal project is and isn't
├── sessions/              ← per-session notes for students
├── reference/             ← background material to dip into when a project needs it
│   ├── python/            ← self-paced Python primer
│   ├── git/               ← version control basics
│   ├── github/            ← sharing and backing up code
│   ├── huggingface/       ← grabbing and running open-weight models
│   ├── pytorch/           ← the framework most modern AI is written in
│   ├── docker/            ← running other people's software cleanly
│   └── papers/            ← a small reading list (Attention Is All You Need, GPT 1–4)
└── examples/              ← full, working example projects you can run, read, or fork
    ├── image_meaning_db/      ← search images by meaning (CLIP + ChromaDB + FastAPI)
    ├── audio_meaning_db/      ← search spoken audio by what's said (Whisper + embeddings)
    └── everything_function/   ← ten "smart Python functions" backed by the same local model call + a browser UI
```

Most of the new entries above are placeholders for now — they'll fill in as the class progresses or as projects pull us toward them.

---

