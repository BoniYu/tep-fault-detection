"""
Human-readable names for TEP's XMEAS (measurement) and XMV (manipulated
variable) columns, from Downs & Vogel (1993), Tables 3-5.
"""

XMEAS_NAMES = {
    1: "A feed rate (stream 1)",
    2: "D feed rate (stream 2)",
    3: "E feed rate (stream 3)",
    4: "A and C feed rate (stream 4)",
    5: "Recycle flow (stream 8)",
    6: "Reactor feed rate (stream 6)",
    7: "Reactor pressure",
    8: "Reactor level",
    9: "Reactor temperature",
    10: "Purge rate (stream 9)",
    11: "Product separator temperature",
    12: "Product separator level",
    13: "Product separator pressure",
    14: "Product separator underflow (stream 10)",
    15: "Stripper level",
    16: "Stripper pressure",
    17: "Stripper underflow (stream 11)",
    18: "Stripper temperature",
    19: "Stripper steam flow",
    20: "Compressor work",
    21: "Reactor cooling water outlet temperature",
    22: "Separator cooling water outlet temperature",
    23: "Reactor feed analysis: Component A",
    24: "Reactor feed analysis: Component B",
    25: "Reactor feed analysis: Component C",
    26: "Reactor feed analysis: Component D",
    27: "Reactor feed analysis: Component E",
    28: "Reactor feed analysis: Component F",
    29: "Purge gas analysis: Component A",
    30: "Purge gas analysis: Component B",
    31: "Purge gas analysis: Component C",
    32: "Purge gas analysis: Component D",
    33: "Purge gas analysis: Component E",
    34: "Purge gas analysis: Component F",
    35: "Purge gas analysis: Component G",
    36: "Purge gas analysis: Component H",
    37: "Product analysis: Component D",
    38: "Product analysis: Component E",
    39: "Product analysis: Component F",
    40: "Product analysis: Component G",
    41: "Product analysis: Component H",
}

XMV_NAMES = {
    1: "D feed flow valve (stream 2)",
    2: "E feed flow valve (stream 3)",
    3: "A feed flow valve (stream 1)",
    4: "A and C feed flow valve (stream 4)",
    5: "Compressor recycle valve",
    6: "Purge valve (stream 9)",
    7: "Separator pot liquid flow valve (stream 10)",
    8: "Stripper liquid product flow valve (stream 11)",
    9: "Stripper steam valve",
    10: "Reactor cooling water flow valve",
    11: "Condenser cooling water flow valve",
}


def describe_column(col_name: str) -> str:
    """Given a column name like 'XMEAS_9' or 'XMV_10', return a readable
    description, e.g. 'XMEAS_9: Reactor temperature'."""
    kind, num = col_name.split("_")
    num = int(num)
    if kind == "XMEAS":
        return f"{col_name}: {XMEAS_NAMES.get(num, 'Unknown')}"
    elif kind == "XMV":
        return f"{col_name}: {XMV_NAMES.get(num, 'Unknown')}"
    return col_name