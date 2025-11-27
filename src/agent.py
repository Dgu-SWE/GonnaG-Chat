import dspy
from typing import Literal
from settings import OPEN_API_KEY
from src.mcp_client import get_mcp_data

lm = dspy.LM("gpt-4o", api_key=OPEN_API_KEY)
dspy.settings.configure(lm=lm)


class RouterSignature(dspy.Signature):
    question = dspy.InputField(desc="사용자 질문")
    intent: Literal["mcp_info", "general"] = dspy.OutputField(desc="의도 분류")


class MCPSummarizerSignature(dspy.Signature):
    """
    당신은 MCP 시스템 관리자입니다.
    'context' 필드에 제공된 데이터는 실제 Spring 서버에서 방금 가져온 정보입니다.

    [지시사항]
    1. 반드시 'context'에 있는 내용을 바탕으로 답변하세요.
    2. 절대로 "외부 서버에 접근할 수 없다"고 말하지 마세요. 데이터는 이미 당신 손에 있습니다.
    3. 데이터를 읽기 좋게 요약해서 설명해주세요.
    """

    context = dspy.InputField(desc="Spring 서버에서 가져온 Raw 데이터")
    question = dspy.InputField(desc="사용자의 질문")
    answer = dspy.OutputField(desc="사용자에게 할 최종 답변")


class RouterAgent(dspy.Module):
    def __init__(self):
        super().__init__()
        self.prog = dspy.ChainOfThought(RouterSignature)

    def forward(self, question: str):
        return self.prog(question=question)


async def process_user_query(user_query: str) -> str:
    router = RouterAgent()
    pred = router(question=user_query)
    intent = pred.intent.lower().strip()

    print(f"[DEBUG] 의도 파악 결과: {intent}")

    if "mcp_info" in intent:
        mcp_data = await get_mcp_data()

        summarizer = dspy.Predict(MCPSummarizerSignature)
        final_answer = summarizer(context=mcp_data, question=user_query)
        return final_answer.answer

    else:
        chat = dspy.Predict("question -> answer")
        return chat(question=user_query).answer
