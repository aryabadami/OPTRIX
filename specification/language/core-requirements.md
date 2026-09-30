# OPTRIX Core Requirements

## R1 — Target Independence

An OPTRIX program must not require target-specific source code for computation that is defined as target-independent.

## R2 — Defined Semantics

Every supported OPTRIX operation must have explicitly defined semantics.

## R3 — Semantic Preservation

A valid compilation path must preserve the semantics defined by the OPTRIX language.

## R4 — Intermediate Representation

The compiler must provide a target-independent intermediate representation capable of representing the required semantics.

## R5 — Target Lowering

The same OPTRIX representation must be capable of being lowered into different execution targets.

## R6 — Verification

The compiler and IR must provide mechanisms for detecting invalid programs and invalid intermediate representations.

## R7 — Reproducibility

Experiments and benchmarks must be reproducible from the repository.

## R8 — Measurement

Claims about correctness, portability, performance, or developer effort must be supported by measurable experiments.

## R9 — Specialization

Target-specific capabilities may be exposed when required, provided their semantics and limitations are explicitly defined.

## R10 — Incremental Expansion

A new execution target must not be considered supported until its compilation and execution path has been implemented and verified.

## R11 — Research Falsifiability

OPTRIX architecture must be allowed to fail experimental hypotheses. Failed experiments must be recorded rather than hidden.

## R12 — Evidence-Based Progress

A roadmap item is complete only when its implementation, test, and required proof exist.
