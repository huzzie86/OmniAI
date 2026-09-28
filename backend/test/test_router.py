from backend.router import classify, choose

def test_classify_coding():
    assert classify("write Python code") == "coding"

def test_classify_research():
    assert classify("research the latest news") == "research"

def test_choose_council():
    assert choose("council", "anything").name == "council"
