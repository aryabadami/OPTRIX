from language.optrix.source import Source, SourceLocation


def test_source_location():
    location = SourceLocation(line=3, column=7)

    assert location.line == 3
    assert location.column == 7


def test_source_returns_requested_line():
    source = Source(
        "let a = 10\nlet b = a + 20",
        "example.opx",
    )

    assert source.line(1) == "let a = 10"
    assert source.line(2) == "let b = a + 20"
    assert source.line(3) == ""


if __name__ == "__main__":
    test_source_location()
    test_source_returns_requested_line()

    print("PASS: source location tests")
