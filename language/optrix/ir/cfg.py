from dataclasses import dataclass, field

from .instructions import (
    Branch,
    Instruction,
    Jump,
    Label,
    Return,
)


@dataclass
class BasicBlock:
    name: str
    instructions: list[Instruction] = field(default_factory=list)
    successors: list[str] = field(default_factory=list)
    predecessors: list[str] = field(default_factory=list)

    def emit(self, instruction: Instruction) -> None:
        self.instructions.append(instruction)

    def add_successor(self, target: str) -> None:
        if target not in self.successors:
            self.successors.append(target)

    def add_predecessor(self, source: str) -> None:
        if source not in self.predecessors:
            self.predecessors.append(source)


@dataclass
class ControlFlowGraph:
    blocks: list[BasicBlock] = field(default_factory=list)

    def add_block(self, block: BasicBlock) -> None:
        self.blocks.append(block)


class CFGBuilder:

    def build(self, function):
        blocks = []
        current = None

        for instruction in function.instructions:

            if isinstance(instruction, Label):
                if current is not None:
                    blocks.append(current)

                current = BasicBlock(instruction.name)
                continue

            if current is None:
                current = BasicBlock("entry")

            current.emit(instruction)

            if isinstance(
                instruction,
                (Jump, Branch, Return),
            ):
                blocks.append(current)
                current = None

        if current is not None:
            blocks.append(current)

        cfg = ControlFlowGraph()

        for block in blocks:
            cfg.add_block(block)

        self._connect(cfg)

        return cfg

    def _connect(self, cfg):
        block_map = {
            block.name: block
            for block in cfg.blocks
        }

        for index, block in enumerate(cfg.blocks):

            if not block.instructions:
                if index + 1 < len(cfg.blocks):
                    block.add_successor(
                        cfg.blocks[index + 1].name
                    )
                continue

            terminator = block.instructions[-1]

            if isinstance(terminator, Jump):
                block.add_successor(
                    terminator.target
                )

            elif isinstance(terminator, Branch):
                block.add_successor(
                    terminator.true_target
                )

                block.add_successor(
                    terminator.false_target
                )

            elif isinstance(terminator, Return):
                # Return terminates execution.
                # It has no successor.
                pass

            elif index + 1 < len(cfg.blocks):
                block.add_successor(
                    cfg.blocks[index + 1].name
                )

        for block in cfg.blocks:
            for successor in block.successors:

                if successor not in block_map:
                    raise ValueError(
                        f"CFG references unknown block: {successor}"
                    )

                block_map[successor].add_predecessor(
                    block.name
                )


class CFGVerificationError(Exception):
    pass


class CFGVerifier:

    def verify(self, cfg: ControlFlowGraph) -> None:
        self._verify_unique_blocks(cfg)
        self._verify_edges(cfg)
        self._verify_bidirectional_edges(cfg)
        self._verify_entry(cfg)

    def _verify_unique_blocks(self, cfg):
        names = set()

        for block in cfg.blocks:
            if block.name in names:
                raise CFGVerificationError(
                    f"Duplicate basic block: {block.name}"
                )

            names.add(block.name)

    def _verify_edges(self, cfg):
        names = {
            block.name
            for block in cfg.blocks
        }

        for block in cfg.blocks:

            for successor in block.successors:
                if successor not in names:
                    raise CFGVerificationError(
                        f"Unknown successor: {successor}"
                    )

            for predecessor in block.predecessors:
                if predecessor not in names:
                    raise CFGVerificationError(
                        f"Unknown predecessor: {predecessor}"
                    )

    def _verify_bidirectional_edges(self, cfg):
        block_map = {
            block.name: block
            for block in cfg.blocks
        }

        for block in cfg.blocks:

            for successor in block.successors:
                target = block_map[successor]

                if block.name not in target.predecessors:
                    raise CFGVerificationError(
                        f"Missing predecessor edge: "
                        f"{block.name} -> {successor}"
                    )

            for predecessor in block.predecessors:
                source = block_map[predecessor]

                if block.name not in source.successors:
                    raise CFGVerificationError(
                        f"Missing successor edge: "
                        f"{predecessor} -> {block.name}"
                    )

    def _verify_entry(self, cfg):
        if not cfg.blocks:
            raise CFGVerificationError(
                "CFG has no basic blocks"
            )
