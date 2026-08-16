import os
from datetime import datetime

def save_raw_text(
    text: str,
    query: str,
    tools_used: str,
    run_id: str,
) -> str:
    output_dir = "outputs"
    os.makedirs(output_dir, exist_ok=True)

    filepath = os.path.join(output_dir, "research_notes.txt")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    record = (
        f"{'=' * 60}\n"
        f"Run ID: {run_id}\n"
        f"Timestamp: {timestamp}\n"
        f"{'=' * 60}\n\n"
        f"Query:\n{query}\n\n"
        f"Tools Used:\n{tools_used}\n\n"
        f"Findings:\n{text}\n\n"
    )

    existing_content = ""

    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            existing_content = f.read()

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(record)
        f.write(existing_content)

    return filepath

