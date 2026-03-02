import re
from typing import Dict, Optional, List, Tuple

SECTION_RE = re.compile(
    r"^\s*(Command\s+Syntax|Parameter(?:s)?|Command\s+Mode|Examples?(?:\s+\d+)?)\s*$",
    re.IGNORECASE
)

def _clean_lines(page_text: str) -> List[str]:
    return [ln.rstrip("\n") for ln in page_text.splitlines()]

def _is_footer_or_header_noise(s: str) -> bool:
    s_strip = s.strip()
    if not s_strip:
        return True

    # Section title pages like "Enhanced Transmission Selection Commands"
    if re.search(r"\bCommands\b\s*$", s_strip, re.IGNORECASE):
        return True

    # Strong footer/header signals
    if re.search(r"(?:\bproprietary\b|\bcopyright\b|\ball\s+rights\s+reserved\b)", s_strip, re.IGNORECASE):
        return True
    if re.search(r"\bIP\s+Infusion\b", s_strip, re.IGNORECASE):
        return True
    if "©" in s_strip or "(c)" in s_strip.lower():
        return True
    if re.search(r"\b(19|20)\d{2}\b", s_strip) and len(s_strip) <= 80:
        return True

    boiler = [
        r"^zebos\b",
        r"^zebos-xp\b",
        r"^command\s+reference\b",
        r"^chapter\s+\d+\b",
        r"^\d+\s*$",
        r"^confidential\b",
    ]
    for pat in boiler:
        if re.search(pat, s_strip, re.IGNORECASE) and len(s_strip) <= 80:
            return True

    # Do not treat anchors as content for description/command_name
    if SECTION_RE.match(s_strip):
        return True

    return False

def _find_sections(lines: List[str]) -> List[Tuple[int, str]]:
    hits: List[Tuple[int, str]] = []
    for i, ln in enumerate(lines):
        m = SECTION_RE.match(ln.strip())
        if not m:
            continue
        hdr = re.sub(r"\s+", " ", m.group(1).strip().lower())
        if hdr.startswith("command syntax"):
            key = "command_syntax"
        elif hdr.startswith("parameter"):
            key = "parameters"
        elif hdr.startswith("command mode"):
            key = "command_mode"
        elif hdr.startswith("example"):
            key = "example"
        else:
            key = hdr
        hits.append((i, key))
    return hits

def _slice_section(lines: List[str], start_idx: int, end_idx: int) -> str:
    body = lines[start_idx + 1 : end_idx]
    while body and not body[0].strip():
        body.pop(0)
    while body and not body[-1].strip():
        body.pop()
    return "\n".join(body).rstrip()

def _guess_command_name_fallback(lines: List[str]) -> Optional[Tuple[int, str]]:
    """
    Return (line_index, command_name) if found, else None.
    This is only used when Command Syntax is missing or we want the actual line position.
    """
    for i, ln in enumerate(lines[:120]):
        s = ln.strip()
        if _is_footer_or_header_noise(s):
            continue
        # Reject sentence-ish lines
        if len(s) > 90 or s.endswith((".", ":", ";")):
            continue
        # Reject syntax lines
        if any(ch in s for ch in "[]{}<>|="):
            continue
        if not re.search(r"[A-Za-z]", s):
            continue
        toks = [t for t in re.split(r"\s+", s) if t]
        if 1 <= len(toks) <= 10:
            return i, re.sub(r"\s+", " ", s)
    return None

def _extract_description_between(lines: List[str], start_i: int, end_i: int) -> Optional[str]:
    """
    Extract non-noise lines between indices (exclusive of start_i, exclusive of end_i).
    """
    buf: List[str] = []
    for ln in lines[start_i + 1 : end_i]:
        s = ln.strip()
        if not s:
            continue
        if _is_footer_or_header_noise(s):
            continue
        # Avoid accidentally pulling in other section headers
        if SECTION_RE.match(s):
            continue
        buf.append(ln.rstrip())
    desc = "\n".join(buf).strip()
    return desc or None

def parse_cmdref_command_page(page_text: str) -> Dict[str, Optional[str]]:
    """
    Parse page into:
      command_name, description, command_syntax, parameters, command_mode, example

    Rules:
      - command_name: prefer first line of command_syntax (most reliable)
      - description: text right under command name and above "Command Syntax"
    """
    lines = _clean_lines(page_text)
    sections = _find_sections(lines)

    out: Dict[str, Optional[str]] = {
        "command_name": None,
        "description": None,
        "command_syntax": None,
        "parameters": None,
        "command_mode": None,
        "example": None,
    }

    # Parse anchored sections
    if sections:
        for idx, (start_i, key) in enumerate(sections):
            end_i = sections[idx + 1][0] if idx + 1 < len(sections) else len(lines)
            content = _slice_section(lines, start_i, end_i)
            if not content:
                continue
            if key == "example":
                out["example"] = (out["example"] + "\n\n" + content).strip() if out["example"] else content.strip()
            else:
                out[key] = (out[key] + "\n\n" + content).strip() if out[key] else content.strip()

    # Find where "Command Syntax" starts (for description extraction)
    cmdsyn_idx = None
    for i, (start_i, key) in enumerate(sections):
        if key == "command_syntax":
            cmdsyn_idx = start_i
            break

    # Determine command_name and the "command name line position" for description slicing
    cmd_name_line_idx: Optional[int] = None

    if out["command_syntax"]:
        first = out["command_syntax"].splitlines()[0].strip()
        out["command_name"] = re.sub(r"\s+", " ", first)
        # Try to find the heading line in the page (optional). If not found, we'll use -1.
        # Sometimes the command name appears as a title line matching the first syntax line partially.
        # We'll fallback to scanning for a plausible heading line.
        cand = _guess_command_name_fallback(lines)
        if cand:
            cmd_name_line_idx = cand[0]
    else:
        cand = _guess_command_name_fallback(lines)
        if cand:
            cmd_name_line_idx, out["command_name"] = cand

    # Extract description
    if cmdsyn_idx is not None:
        # Prefer: between command name line (if we have it) and Command Syntax header
        if cmd_name_line_idx is not None and cmd_name_line_idx < cmdsyn_idx:
            out["description"] = _extract_description_between(lines, cmd_name_line_idx, cmdsyn_idx)
        else:
            # Fallback: take top-of-page non-noise content before Command Syntax
            # Use start index -1 meaning "from beginning"
            pseudo_start = -1
            out["description"] = _extract_description_between(lines, pseudo_start, cmdsyn_idx)

    return out


# Quick test
if __name__ == "__main__":
    sample = """
Enhanced Transmission Selection Commands

show enhanced-transmission-selection interface IFNAME
Displays ETS status for an interface.

Command Syntax
show enhanced-transmission-selection interface IFNAME

Parameter
IFNAME
Name of the interface.

Command Mode
Exec mode

Example 1
#show enhanced-transmission-selection interface eth1
Interface : eth1
"""
    parsed = parse_cmdref_command_page(sample)
    for k, v in parsed.items():
        print("==", k)
        print(v)

# Quick test (similar to your case)

if __name__ == "__main__":
    import fitz
    # Quick test on a real PDF page (adjust path as needed
    docs = fitz.open("/home/tuanpm/Agentic_new/ZebOS-XP_1.4_PDFs/PDF/ZebOS_DCB_CmdRef.pdf")
    
    sample_page = docs[34].get_text()  # adjust page index as needed
    parsed = parse_cmdref_command_page(sample_page)
    for k, v in parsed.items():
        print("==", k)
        print(v)