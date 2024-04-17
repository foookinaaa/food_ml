from mlops_ods.app.example import is_positive


def test_is_positive_true():
    assert is_positive(5) is True


def test_is_positive_false():
    assert is_positive(-5) is False
