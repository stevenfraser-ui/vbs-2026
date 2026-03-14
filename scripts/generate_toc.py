import sys
import os

def generate_toc(filename):
    if not os.path.exists(filename):
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)

    base_name, _ = os.path.splitext(filename)
    out_filename = f"{base_name}-toc.md"

    toc_entries = []
    current_night = None
    current_act = None
    current_start = None

    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith("# Night "):
            if current_night and current_act:
                toc_entries.append(f"{current_night} {current_act} - {current_start}:{i-1}")
            current_night = stripped.replace("# ", "").strip()
            current_act = None
            current_start = i
        elif stripped.startswith("## Act "):
            if current_act is not None:
                toc_entries.append(f"{current_night} {current_act} - {current_start}:{i-1}")
                current_start = i
            current_act = stripped.replace("## ", "").strip()

    if current_night and current_act:
        toc_entries.append(f"{current_night} {current_act} - {current_start}:{len(lines)}")

    with open(out_filename, 'w', encoding='utf-8') as f:
        for entry in toc_entries:
            f.write(entry + "\n")

    print(f"Generated {out_filename}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generate_toc.py <filename>")
        sys.exit(1)
    
    generate_toc(sys.argv[1])
