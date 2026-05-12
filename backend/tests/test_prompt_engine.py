from app.services.prompt_engine import find_prompt_variables, render_prompt


def test_find_prompt_variables():
    assert find_prompt_variables("账号{account_persona}写给{target_audience}") == [
        "account_persona",
        "target_audience",
    ]


def test_render_prompt_missing_and_present():
    rendered, missing = render_prompt("你好 {name}，请写 {topic}", {"name": "小红贸"})
    assert rendered == "你好 小红贸，请写 {topic}"
    assert missing == ["topic"]
