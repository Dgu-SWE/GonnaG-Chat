import dspy
from typing import Literal


class RouterSignature(dspy.Signature):
    """
    사용자의 질문을 분석하여 가장 적절한 의도(intent)를 분류합니다.

    1. user_info: 사용자의 이름, 학번, 학점, 전공 등 개인 정보를 물어보는 경우
    2. graduation: 졸업 요건, 남은 학점, 졸업 가능 여부 등
    3. announcement: 학교 공지사항, 장학금 공지 등
    4. recommendation: 수업 추천, 꿀교양 등
    5. test: 시스템 테스트 관련
    6. general: 그 외 일상 대화
    """

    question = dspy.InputField(desc="사용자의 질문")
    intent: Literal[
        "user_info",
        "graduation",
        "announcement",
        "recommendation",
        "test",
        "general",
    ] = dspy.OutputField(desc="의도 분류 결과")


class UserInfoSignature(dspy.Signature):
    """
    당신은 학사 정보 관리자입니다.
    제공된 'user_data'(학생 정보)를 바탕으로 사용자의 질문에 친절하게 답변하세요.
    """

    user_data = dspy.InputField(desc="조회된 학생 정보")
    question = dspy.InputField(desc="사용자의 질문")
    answer = dspy.OutputField(desc="답변")


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


class TestMcpSignature(dspy.Signature):
    """당신은 SPRING 서버에 구현된 mcp를 호출할 수 있습니다. /mcp로 요청하면 테스트 결과를 확인할 수 있습니다. 실행결과를 보고하세요"""

    result = dspy.InputField(desc="실행결과")
    question = dspy.InputField(desc="질문")
    answer = dspy.OutputField(desc="외부 서버 mcp 실행에대한 결과 보고")
