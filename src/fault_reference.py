"""
Reference for the 20 TEP faults (IDV 1-20), from Downs & Vogel (1993),
Table 8. Fault 0 = normal operation (not a real fault).
"""

FAULT_DESCRIPTIONS = {
    0: ("Normal operation", "None"),
    1: ("A/C feed ratio, B composition constant (stream 4)", "Step"),
    2: ("B composition, A/C ratio constant (stream 4)", "Step"),
    3: ("D feed temperature (stream 2)", "Step"),
    4: ("Reactor cooling water inlet temperature", "Step"),
    5: ("Condenser cooling water inlet temperature", "Step"),
    6: ("A feed loss (stream 1)", "Step"),
    7: ("C header pressure loss - reduced availability (stream 4)", "Step"),
    8: ("A, B, C feed composition (stream 4)", "Random variation"),
    9: ("D feed temperature (stream 2)", "Random variation"),
    10: ("C feed temperature (stream 4)", "Random variation"),
    11: ("Reactor cooling water inlet temperature", "Random variation"),
    12: ("Condenser cooling water inlet temperature", "Random variation"),
    13: ("Reaction kinetics", "Slow drift"),
    14: ("Reactor cooling water valve", "Sticking"),
    15: ("Condenser cooling water valve", "Sticking"),
    16: ("Unknown", "Unknown"),
    17: ("Unknown", "Unknown"),
    18: ("Unknown", "Unknown"),
    19: ("Unknown", "Unknown"),
    20: ("Unknown", "Unknown"),
}

# Widely cited (Chiang, Russell & Braatz, 2001) as statistically
# undetectable in this dataset's noise level.
HARD_TO_DETECT_FAULTS = [3, 9, 15]


def describe(fault_number: int) -> str:
    desc, ftype = FAULT_DESCRIPTIONS.get(fault_number, ("Unknown fault", "Unknown"))
    return f"Fault {fault_number}: {desc} ({ftype})"