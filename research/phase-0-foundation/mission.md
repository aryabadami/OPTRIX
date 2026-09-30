# OPTRIX — Mission

## Ultimate Mission

OPTRIX aims to investigate and build a universal programming system in which humans and AI can express computation through a coherent programming model, while preserving the defined meaning of that computation and enabling execution across fundamentally different hardware and environments.

## Core Problem

Modern computing is fragmented across different programming models, compilers, runtimes, APIs, and hardware-specific execution environments.

OPTRIX investigates whether computational meaning can be separated sufficiently from physical execution so that the same program can be systematically lowered to different execution targets without unnecessary source-level rewriting.

## Core Idea

OPTRIX separates:

1. What a computation means.
2. How that computation is represented.
3. How that computation is executed on a particular target.

The intended architecture is:

Program
  ↓
Semantics
  ↓
OPTRIX IR
  ↓
Target-specific lowering
  ↓
Backend
  ↓
Runtime
  ↓
Execution

## Initial Proof

The first major engineering objective is to demonstrate a small OPTRIX program executing correctly across multiple substantially different targets.

Initial targets:

- CPU
- GPU
- WASM

The exact workload will be selected during Phase 4.

## Success

OPTRIX succeeds experimentally when a single program can be represented and executed across multiple targets while:

- preserving defined semantics,
- minimizing unnecessary target-specific source changes,
- providing measurable performance,
- and allowing reproducible verification.

## Research Principle

OPTRIX is a hypothesis-driven engineering project.

A hypothesis is not considered true because it sounds architecturally reasonable.

It must be implemented, tested, measured, and verified.

Failure is a valid research result when it identifies a fundamental limitation or boundary.

## Long-Term Direction

The long-term objective is to evolve OPTRIX from a programming language into a complete programming system containing:

- a programming model,
- semantic system,
- universal IR,
- compiler,
- multiple backends,
- correctness infrastructure,
- intelligent compilation,
- hardware specialization,
- runtime,
- and eventually AI-assisted program generation.

These capabilities will be developed only after the preceding layers have been experimentally validated.
