from .frame import ExecutionFrame


class CallStack:

    def __init__(self) -> None:
        self._frames: list[ExecutionFrame] = []

    def push(self, frame: ExecutionFrame) -> None:
        self._frames.append(frame)

    def pop(self) -> ExecutionFrame:
        if not self._frames:
            raise RuntimeError(
                "Cannot pop from empty call stack"
            )

        return self._frames.pop()

    def peek(self) -> ExecutionFrame:
        if not self._frames:
            raise RuntimeError(
                "Cannot peek at empty call stack"
            )

        return self._frames[-1]

    def is_empty(self) -> bool:
        return len(self._frames) == 0

    def depth(self) -> int:
        return len(self._frames)

    def clear(self) -> None:
        self._frames.clear()
