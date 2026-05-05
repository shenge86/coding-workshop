# PyTorch — reference material

*Placeholder.* This folder will cover PyTorch: the framework most modern AI models are written in. You don't need to know PyTorch to *use* a model, but you'll see it everywhere once you start poking around.

Planned topics:

- What a tensor is, and why it's basically a multi-dimensional array
- Moving tensors between CPU and GPU (and what to do if you don't have a GPU)
- Loading a pretrained model and running inference
- The shape of a forward pass, conceptually
- `torch.no_grad()` — and when it matters
- Reading a model architecture without panicking
- A very gentle intro to training and fine-tuning (separate file, optional)
- CPU-only PyTorch installs vs. CUDA installs — which one you actually want

## When to dip in

When you find yourself reading model code and the lines starting with `torch.` are blocking you, or when you want to fine-tune something on your own data.

## When *not* to dip in

If you only ever call models through a high-level API (Hugging Face `pipeline()`, an OpenAI-compatible client, etc.), you may never need this.

## Prerequisites

Comfort with [`../python/`](../python/), especially classes and basic data structures.
