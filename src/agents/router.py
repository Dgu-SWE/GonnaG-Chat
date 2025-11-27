import dspy
from src.agents.signatures import RouterSignature


class RouterAgent(dspy.Module):
    def __init__(self, callbacks=None):
        super().__init__(callbacks)

        self.prog = dspy.ChainOfThought(RouterSignature)

    def forward(self, question: str):
        return self.prog(question=question)
