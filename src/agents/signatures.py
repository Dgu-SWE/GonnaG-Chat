import dspy
from typing import Literal


class RouterSignature(dspy.Signature):
    """
    사용자의 질문을 분석하여 가장 적절한 담당 에이전트의 의도(intent)를 분류합니다.
    """

    question = dspy.InputField(desc="사용자의 질문")
    intent: Literal[
        "graduation", "announcement", "recommendation", "general", "test"
    ] = dspy.OutputField(desc="의도 분류 결과")


class GraduationSignature(dspy.Signature):
    """
    당신은 학사 관리 전문가입니다.
    제공된 'user_info'(내 성적)와 'guide'(졸업 요건)를 비교 분석하여 졸업 가능 여부를 판단하고 답변하세요.
    """

    user_info = dspy.InputField(desc="사용자 정보")
    guide = dspy.InputField(desc="졸업 요건 가이드")
    question = dspy.InputField(desc="질문")
    answer = dspy.OutputField(desc="답변")


class AnnouncementSignature(dspy.Signature):
    """
    당신은 학교 소식통입니다. 'announcements' 목록에서 질문과 관련된 정보를 요약해 주세요.
    """

    announcements = dspy.InputField(desc="공지사항 목록")
    question = dspy.InputField(desc="질문")
    answer = dspy.OutputField(desc="답변")


class RecommendationSignature(dspy.Signature):
    """
    당신은 수강신청 멘토입니다. 'user_info'(전공 등)와 'class_list'를 고려하여 적절한 수업을 추천하세요.
    """

    user_info = dspy.InputField(desc="사용자 정보")
    class_list = dspy.InputField(desc="수업 목록")
    question = dspy.InputField(desc="질문")
    answer = dspy.OutputField(desc="답변")


class TestMcpSiganture(dspy.Signature):
    """당신은 SPRING 서버에 구현된 mcp를 호출할 수 있습니다. /mcp로 요청하면 테스트 결과를 확인할 수 있습니다. 실행결과를 보고하세요"""
    result = dspy.InputField(desc="실행결과")
    question = dspy.InputField(desc="질문")
    answer = dspy.OutputField(desc="외부 서버 mcp 실행에대한 결과 보고")