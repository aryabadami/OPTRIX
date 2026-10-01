# Compiler Fundamentals Laboratory

## Objective

Experimentally understand the difference between:

- interpretation
- compilation
- code generation
- transpilation
- execution

## Experiments

### Interpreter

Source expression:

2 + 3

Execution:

source -> parser -> interpreter -> result

Result:

5

### Compiler

Source:

2 + 3

Generated representation:

PUSH 2
PUSH 3
ADD

Execution:

source -> compiler -> generated instructions -> executor -> result

Result:

5

### Transpiler

Source:

2 + 3

Generated Python:

print(2 + 3)

Execution:

source -> transpiler -> Python -> Python runtime -> result

Result:

5

## Key Observation

Compilation and interpretation are different execution strategies.

A compiler transforms a program into another executable representation before execution.

An interpreter directly executes the program's semantics.

A transpiler translates one source representation into another source representation.

## OPTRIX Relevance

OPTRIX will eventually need to separate:

1. source representation
2. semantic representation
3. intermediate representation
4. target representation
5. runtime execution
