from ..ast import (
    BinaryExpression,
    BooleanLiteral,
    Identifier,
    IntegerLiteral,
    Block,
    IfStatement,
    LetStatement,
    Program,
    UnaryExpression,
    WhileStatement,
)

from .instructions import (
    BinaryOp,
    Branch,
    ConstBool,
    ConstInt,
    Jump,
    Label,
    Load,
    Store,
    UnaryOp,
)

from .module import IRFunction, IRModule


class IRLoweringError(Exception):
    pass


class Lowerer:
    def __init__(self):
        self._temp_counter = 0
        self._label_counter = 0

    def _new_temp(self) -> str:
        name = f"%{self._temp_counter}"
        self._temp_counter += 1
        return name

    def _new_label(self, prefix: str) -> str:
        name = f"{prefix}_{self._label_counter}"
        self._label_counter += 1
        return name

    def lower(self, program: Program) -> IRModule:
        function = IRFunction("main")

        for statement in program.statements:
            self._lower_statement(statement, function)

        module = IRModule()
        module.add_function(function)

        return module

    def _lower_statement(self, statement, function):
        if isinstance(statement, LetStatement):
            value = self._lower_expression(statement.value, function)
            function.emit(Store(statement.name, value))
            return

        if isinstance(statement, IfStatement):
            condition = self._lower_expression(
                statement.condition,
                function,
            )

            then_label = self._new_label("then")
            else_label = self._new_label("else")
            merge_label = self._new_label("merge")

            function.emit(
                Branch(
                    condition,
                    then_label,
                    else_label,
                )
            )

            function.emit(Label(then_label))

            self._lower_block(
                statement.then_branch,
                function,
            )

            function.emit(Jump(merge_label))

            function.emit(Label(else_label))

            if statement.else_branch is not None:
                self._lower_block(
                    statement.else_branch,
                    function,
                )

            function.emit(Jump(merge_label))
            function.emit(Label(merge_label))

            return

        if isinstance(statement, WhileStatement):
            loop_label = self._new_label("loop")
            body_label = self._new_label("body")
            exit_label = self._new_label("exit")

            function.emit(Label(loop_label))

            condition = self._lower_expression(
                statement.condition,
                function,
            )

            function.emit(
                Branch(
                    condition,
                    body_label,
                    exit_label,
                )
            )

            function.emit(Label(body_label))

            self._lower_block(
                statement.body,
                function,
            )

            function.emit(Jump(loop_label))
            function.emit(Label(exit_label))

            return

        raise IRLoweringError(
            f"Unsupported statement: {type(statement).__name__}"
        )

    def _lower_block(self, block: Block, function):
        for statement in block.statements:
            self._lower_statement(statement, function)

    def _lower_expression(self, expression, function) -> str:
        if isinstance(expression, IntegerLiteral):
            result = self._new_temp()
            function.emit(ConstInt(result, expression.value))
            return result

        if isinstance(expression, BooleanLiteral):
            result = self._new_temp()
            function.emit(ConstBool(result, expression.value))
            return result

        if isinstance(expression, Identifier):
            result = self._new_temp()
            function.emit(Load(result, expression.name))
            return result

        if isinstance(expression, UnaryExpression):
            operand = self._lower_expression(expression.operand, function)
            result = self._new_temp()

            function.emit(
                UnaryOp(
                    result=result,
                    operator=expression.operator,
                    operand=operand,
                )
            )

            return result

        if isinstance(expression, BinaryExpression):
            left = self._lower_expression(expression.left, function)
            right = self._lower_expression(expression.right, function)

            result = self._new_temp()

            function.emit(
                BinaryOp(
                    result=result,
                    operator=expression.operator,
                    left=left,
                    right=right,
                )
            )

            return result

        raise IRLoweringError(
            f"Unsupported expression: {type(expression).__name__}"
        )
