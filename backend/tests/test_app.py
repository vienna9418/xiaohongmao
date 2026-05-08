from app.main import create_app


def test_create_app():
    app = create_app()
    assert app.title == "小红贸 API"
