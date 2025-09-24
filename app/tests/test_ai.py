def test_ai_smoke():
    """Teste smoke básico"""
    assert True

def test_ai_import():
    """Teste que as importações funcionam"""
    try:
        from app.routes import ai
        assert ai is not None
    except ImportError:
        assert False, "Erro na importação"
