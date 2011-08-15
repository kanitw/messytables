from collections import defaultdict

from messytables.core import Cell

def column_count_modal(rows):
    """ Return the modal value of columns in the row_set's 
    sample. This can be assumed to be the number of columns
    of the table. """
    counts = defaultdict(int)
    for row in rows:
        length = len([c for c in row if not c.empty])
        counts[length] += 1
    if not len(counts):
        return 0
    return max(counts.items(), key=lambda (k,v): v)[0]

def headers_guess(rows, tolerance=1):
    """ Guess the offset and names of the headers of the row set.
    This will attempt to locate the first row within ``tolerance``
    of the mode of the number of rows in the row set sample.

    The return value is a tuple of the offset of the header row
    and the names of the columns.
    """
    rows = list(rows)
    modal = column_count_modal(rows)
    for i, row in enumerate(rows):
        length = len([c for c in row if not c.empty])
        if length >= modal - tolerance:
            # TODO: use type guessing to check that this row has
            # strings and does not conform to the type schema of 
            # the table.
            return i,  [c.value for c in row]
    return 0, []

from itertools import izip_longest
def headers_processor(headers):
    """ Add column names to the cells in a row_set. If no header is 
    defined, use an autogenerated name. """
    def apply_headers(row_set, row):
        _row = []
        pairs = izip_longest(row, headers)
        for i, (cell, header) in enumerate(pairs):
            if cell is None:
                cell = Cell(None)
            cell.column = header
            if cell.column is None or not len(cell.column):
                cell.column = "column_%d" % i
                cell.column_autogenerated = True
            _row.append(cell)
        return _row
    return apply_headers

