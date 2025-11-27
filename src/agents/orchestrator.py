import dspy
from src.config import OPEN_API_KEY
from src.services.mcp_client import *
from src.agents.signatures import *
from src.agents.router import RouterAgent

lm = dspy.LM("openai/gpt-4o", api_key=OPEN_API_KEY)
dspy.configure(lm=lm)


async def process_user_query(user_query: str, user_id: int) -> str:
    router = RouterAgent()
    pred = router(question=user_query)
    intent = pred.intent.lower().strip()

    print(f"[Debug] 의도 분석 {intent}")

    if "graduiation" in intent:
        user_data = await fetch_user_info(user_id)
        guide_data = await fetch_academic_guide(user_id)

        agent = dspy.Predict(GraduationSignature)
        res = agent(user_info=user_data, guide=guide_data, question=user_query)
        return res.answer
    elif "announcement" in intent:
        news_data = await fetch_announcements(id)

        agent = dspy.Predict(AnnouncementSignature)
        res = agent(announcements=news_data, question=user_query)
        return res.answer

    elif "recommendation" in intent:
        user_data = await fetch_user_info(id)
        classes_data = await fetch_class_info(id)

        agent = dspy.Predict(RecommendationSignature)
        res = agent(user_info=user_data, class_list=classes_data, question=user_query)
        return res.answer

    elif "general" in intent:
        agent = dspy.Predict("question -> answer")
        res = agent(question=user_query)
        return res.answer

    elif "test" in intent:
        response = await test_mcp()
        agent = dspy.Predict(TestMcpSiganture)
        res = agent(result=response, question=user_query)
        return res.answer
