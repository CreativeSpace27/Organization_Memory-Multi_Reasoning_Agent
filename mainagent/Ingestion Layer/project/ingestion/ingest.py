# ingestion/ingest.py
from ingestion.loader import load_text
from ingestion.chunker import chunk_text
from ingestion.decision_extractor import extract_decision
from ingestion.send_to_brain import send_to_brain

def ingest(file_path):
    print("📥 Loading file...")
    text = load_text(file_path)

    print("✂️ Chunking text...")
    chunks = chunk_text(text)

    print(f"🔍 Processing {len(chunks)} chunks...\n")

    seen_decisions = set()

    for i, chunk in enumerate(chunks):
        print(f"--- Chunk {i+1} ---")

        result = extract_decision(chunk)

        if result:
            decision = result["decision"]

            # 🔁 Deduplication
            if decision in seen_decisions:
                print("⚠️ Duplicate decision skipped\n")
                continue

            seen_decisions.add(decision)

            result["source"] = file_path

            print("🧠 Extracted Decision:", result, "\n")

            send_to_brain(result)

    print("✅ Ingestion Complete")


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("❌ Usage: python ingest.py <file_path>")
    else:
        ingest(sys.argv[1])




def process_raw_text(text, source_name):
    """
    Yeh function API se aane waale text ko process karega.
    """
    print(f"✂️ Chunking text from {source_name}...")
    chunks = chunk_text(text)
    
    results = []
    for chunk in chunks:
        result = extract_decision(chunk)
        if result and result.get("decision") != "Manual Check Required":
            result["source"] = source_name
            print(f"🧠 Extracted: {result['decision']}")
            send_to_brain(result)
            results.append(result)
    return results