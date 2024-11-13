from __future__ import print_function
import heapq
import itertools

__all__ = ['RangeSet']


class RangeSet:
    """A RangeSet represents a set of non-overlapping ranges on the
    integers, optimized for ranges with many continuous blocks.
    """

    def __init__(self, data=None):
        self.monotonic = False
        if isinstance(data, str):
            self._parse_internal(data)
        elif data:
            assert len(data) % 2 == 0, "Data should contain even number of elements"
            self.data = tuple(self._remove_pairs(data))
            self.monotonic = all(x < y for x, y in zip(self.data, self.data[1:]))
        else:
            self.data = ()

    def __iter__(self):
        return (self.data[i : i + 2] for i in range(0, len(self.data), 2))

    def __eq__(self, other):
        return self.data == other.data

    def __bool__(self):
        return bool(self.data)

    def __str__(self):
        return self.to_string() if self.data else 'empty'

    def __repr__(self):
        return f'<RangeSet("{self.to_string()}")>'

    @classmethod
    def parse(cls, text):
        """Parse a space-separated list of ranges or blocks, returning a RangeSet object."""
        return cls(text)

    def _parse_internal(self, text):
        data = []
        last = -1
        monotonic = True
        for p in text.split():
            s, e = (map(int, p.split('-')) if '-' in p else (int(p), int(p)))
            data.extend((s, e + 1))
            monotonic = monotonic and last <= s <= e
            last = e if last <= s <= e else last
        data.sort()
        self.data = tuple(self._remove_pairs(data))
        self.monotonic = monotonic

    @staticmethod
    def _remove_pairs(source):
        """Remove consecutive duplicate items to simplify the result."""
        last = None
        for i in source:
            if i != last:
                if last is not None:
                    yield last
                last = i
        if last is not None:
            yield last

    def to_string(self):
        return ' '.join(
            f"{s}" if e == s + 1 else f"{s}-{e - 1}"
            for s, e in self
        )

    def to_string_raw(self):
        return f"{len(self.data)},{','.join(map(str, self.data))}"

    def union(self, other):
        """Return a new RangeSet representing the union of this RangeSet with the argument."""
        return self._combine_with(other, add_op=True)

    def intersect(self, other):
        """Return a new RangeSet representing the intersection of this RangeSet with the argument."""
        return self._combine_with(other, add_op=False)

    def subtract(self, other):
        """Return a new RangeSet representing subtracting the argument from this RangeSet."""
        return self._combine_with(other, add_op=False, subtract=True)

    def overlaps(self, other):
        """Return True if the argument overlaps with this RangeSet."""
        z = 0
        for _, d in heapq.merge(zip(self.data, itertools.cycle((+1, -1))),
                                zip(other.data, itertools.cycle((+1, -1)))):
            if (z == 1 and d == 1) or (z == 2 and d == -1):
                return True
            z += d
        return False

    def size(self):
        """Return the total count of integers in the RangeSet."""
        return sum((e - s) for s, e in self)

    def map_within(self, other):
        """Return a RangeSet representing the 'other' mapped within this RangeSet starting at zero."""
        out, offset, start = [], 0, None
        for p, d in heapq.merge(zip(self.data, itertools.cycle((-5, +5))),
                                zip(other.data, itertools.cycle((-1, +1)))):
            if d == -5:
                start = p
            elif d == +5:
                offset += p - start
                start = None
            else:
                out.append(offset + p - start)
        return RangeSet(data=out)

    def extend(self, n):
        """Extend the RangeSet by 'n' blocks."""
        return RangeSet(' '.join(f"{max(0, s - n)}-{e + n - 1}" for s, e in self))

    def first(self, n):
        """Return a RangeSet containing up to the first 'n' integers."""
        if self.size() <= n:
            return self
        out = []
        for s, e in self:
            if e - s >= n:
                out += (s, s + n)
                break
            out += (s, e)
            n -= e - s
        return RangeSet(data=out)

    def _combine_with(self, other, add_op=True, subtract=False):
        """Utility to combine RangeSets with union, intersect or subtract operations."""
        out, z = [], 0
        cycle = itertools.cycle((+1, -1) if add_op else ((-1, +1) if subtract else (+1, -1)))
        for p, d in heapq.merge(zip(self.data, itertools.cycle((+1, -1))),
                                zip(other.data, cycle)):
            if (z == 0 and d == 1) or (z == 1 and d == -1):
                out.append(p)
            z += d
        return RangeSet(data=out)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
