import dspy
from typing import Literal
from settings import OPEN_API_KEY
from mcp_client import get_mcp_data

lm = dspy.OpenAI(model="gpt-4o", api_key=OPEN_API_KEY)
dspy.settings.config(lm=lm)


class RouterSignature(dspy.Signature):
    question = dspy.InputField(desc="사용자 질문")
    intent: Literal["mcp_info", "general"] = dspy.OutputField(desc="의도 분류")

