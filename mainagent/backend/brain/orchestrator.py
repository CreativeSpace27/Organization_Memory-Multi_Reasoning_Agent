from brain.vector_store import VectorStore
from brain.reasoning_agent import ReasoningAgent
from brain.retrieval_agent import RetrievalAgent
from brain.answer_agent import AnswerAgent
from brain.impact_agent import ImpactAgent
import uuid

class BrainOrchestrator:

    def __init__(self):
        self.memory = VectorStore()
        self.reasoner = ReasoningAgent()
        self.retriever = RetrievalAgent()
        self.answer_agent = AnswerAgent()
        self.impact_agent = ImpactAgent()

    def store_decision(self, data):
        decision = data.get("decision")
        reason = data.get("reason") or data.get("reasoning", [])
        source = data.get("source", "manual")
        alternatives = data.get("alternatives", [])
        impacts = data.get("impacts", [])

        # Convert lists to strings to avoid ChromaDB TypeError
        reason_str = ", ".join(reason) if isinstance(reason, list) else str(reason)
        alternatives_str = ", ".join(alternatives) if isinstance(alternatives, list) else str(alternatives)
        impacts_str = ", ".join(impacts) if isinstance(impacts, list) else str(impacts)

        text = f"""Decision: {decision}
Reason: {reason_str}
Alternatives: {alternatives_str}
Impacts: {impacts_str}
Source: {source}"""

        metadata = {
            "decision": str(decision) if decision else "",
            "reason": reason_str,
            "alternatives": alternatives_str,
            "impacts": impacts_str,
            "source": str(source)
        }

        self.memory.store(text, metadata)
        return {"status": "stored"}

    def ask_question(self, question):
        # Correctly indented inside the method
        context, metadata = self.retriever.retrieve(
            self.memory,
            question
        )

        if not context:
            return {
                "answer": "No decision found.",
                "sources": []
            }

        # Detect impact question
        if "what if" in question.lower() or "remove" in question.lower():
            reasoning = self.impact_agent.analyze(
                question,
                context
            )
        else:
            reasoning = self.reasoner.reason(
                question,
                context
            )

        return self.answer_agent.build(
            reasoning,
            metadata
        )