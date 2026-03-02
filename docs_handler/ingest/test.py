from detect_entries import parse_cmdref_command_page
import fitz

def test_detect_command_entries():
    docs = fitz.open("/home/tuanpm/Agentic_new/ZebOS-XP_1.4_PDFs/PDF/ZebOS_DCB_CmdRef.pdf")
    entries = []
    for i in range(len(docs)):
        page_text = docs[i].get_text()
        parsed = parse_cmdref_command_page(page_text)
        if parsed["command_name"]:
            entries.append(parsed)
            print(f"Page {i}: Found command '{parsed['command_name']}' with description '{parsed['description']}' and syntax length {len(parsed['command_syntax']) if parsed['command_syntax'] else 0}")
    print(f"Found {len(entries)} command entries")



if __name__ == "__main__":
    test_detect_command_entries()