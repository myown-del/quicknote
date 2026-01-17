import pytest

from brain.domain.value_objects import LinkInterval


def test_link_interval_length_returns_span():
    # setup: create interval with start and end
    interval = LinkInterval(start=3, end=8)

    # action: read length property
    length = interval.length

    # check: length equals end minus start
    assert length == 5


def test_link_interval_orders_by_start():
    # setup: create two intervals with different starts
    earlier = LinkInterval(start=1, end=4)
    later = LinkInterval(start=2, end=5)

    # action: compare intervals
    is_less = earlier < later

    # check: comparison uses start position
    assert is_less is True


def test_link_interval_lt_rejects_other_types():
    # setup: create interval and incompatible object
    interval = LinkInterval(start=1, end=2)
    other = 5

    # action: attempt comparison with unsupported type
    # check: comparison raises because type is unsupported
    with pytest.raises(TypeError):
        _ = interval < other
