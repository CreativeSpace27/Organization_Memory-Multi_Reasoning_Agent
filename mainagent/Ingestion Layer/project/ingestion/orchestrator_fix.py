# Fixed orchestrator.py - Copy this to backend/brain/orchestrator.py

def store_decision(self, data):
    decision = data.get("decision")
    reason = data.get("reason") or data.get("reasoning", [])  # Handle both 'reason' and 'reasoning'
    source = data.get("source", "manual")
    alternatives = data.get("alternatives", [])
    impacts = data.get("impacts", [])
    
    # Convert lists to strings for display
    reason_str = ", ".join(reason) if isinstance(reason, list) else reason
    alternatives_str = ", ".join(alternatives) if isinstance(alternatives, list) else str(alternatives)
    impacts_str = ", ".join(impacts) if isinstance(impacts, list) else str(impacts)
    
    text = f"""Decision: {decision}
Reason: {reason_str}
Alternatives: {alternatives_str}
Impacts: {impacts_str}
Source: {source}"""
    
    metadata = {
        "decision": decision,
        "reason": reason,  # Will be converted to string in VectorStore
        "alternatives": alternatives,  # Will be converted to string in VectorStore
        "impacts": impacts,  # Will be converted to string in VectorStore
        "source": source
    }
    
    self.memory.store(text, metadata)
    return {"status": "stored"}
