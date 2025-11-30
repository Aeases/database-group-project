# source https://stackoverflow.com/questions/37051516/printing-a-properly-formatted-sqlite-table-in-python
# this is purely to print out the sql results in a nice human readable format.
import sqlite3
import sys

def print_cursor(
    cursor: sqlite3.Cursor,
    *,
    first: int = 1000,
    last: int = 0,
    show_header: bool = True,
    show_count: bool = True,
    total_width: int = 80,
    max_width: int = 25,
    stream = sys.stdout,
):
    # name of each column
    header = [x[0] for x in cursor.description]
    # width of the repr of each column
    widths = [min(len(x), max_width) for x in header]

    # iterate over the whole Cursor, but only keep `first + 2*last` rows in memory
    first_rows = []
    last_rows = []
    row_count = 0
    for row in cursor:
        if len(first_rows) < first + last:
            first_rows.append(row)
        last_rows.append(row)
        if len(last_rows) > last:
            last_rows = last_rows[1:]
        row_count += 1

    if row_count <= first + last:
        # if the number of rows <= `first + last`, show them all
        rows = first_rows
    else:
        # otherwise, show the `first`, an ellipsis row, and then `last`
        rows = first_rows[:first] + [[...] * len(header)] + last_rows

    # represent rows with mutable lists so that we can replace them with reprs
    rows = [list(x) for x in rows]

    align = [">"] * len(header)
    for row in rows:
        assert len(row) == len(header), f"{len(row)} columns != {len(header)} columns"
        for i, cell in enumerate(row):
            # if all values are str or bytes (ignoring None), left-align
            if cell != ... and isinstance(cell, (str, bytes)) and cell is not None:
                align[i] = "<"
            # replace data with their repr strings (except ellipsis)
            row[i] = "..." if cell == ... else repr(cell)
            # identify the maximum (string) width of each column, up to max_width
            widths[i] = min(max(widths[i], len(row[i])), max_width)

    # if the table is too wide, replace the last column with ellipsis
    if sum(widths) + (len(widths) - 1) * 2 > total_width:
        header[-1] = "..."
        widths[-1] = 3
        for row in rows:
            row[-1] = "..."

    # if the table is still too wide, remove columns
    while sum(widths) + (len(widths) - 1) * 2 > total_width and len(header) > 1:
        del header[-2]
        del widths[-2]
        for row in rows:
            del row[-2]

    # prepare a format string for each line of text
    formatter = " | ".join(f"{{:{a}{w}s}}" for a, w in zip(align, widths))
    # prepare the horizontal line between header and data
    header_separator = "-+-".join("-" * w for w in widths)

    if show_header:
        # print the table column names and a horizontal line under it
        stream.write(formatter.format(*[x[:w] for x, w in zip(header, widths)]) + "\n")
        stream.write(header_separator + "\n")
    for row in rows:
        # print each table row
        stream.write(formatter.format(*[x[:w] for x, w in zip(row, widths)]) + "\n")
    if show_count:
        # print the number of rows in another horizontal line
        count = f"--- {row_count} rows ---"
        stream.write(count + header_separator[len(count) :] + "\n")
