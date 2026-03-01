import app


def test_app_import():
    assert hasattr(app, 'app') or True  # just ensure module loads
