from dataclasses import dataclass

@dataclass
class Route:
    name: str
    reason: str

def classify(message: str) -> str:
    text = message.lower()
    if any(k in text for k in ["code", "python", "javascript", "bug", "program"]):
        return "coding"
    if any(k in text for k in ["image", "photo", "picture", "vision"]):
        return "vision"
    if any(k in text for k in ["latest", "today", "research", "sources", "search"]):
        return "research"
    if any(k in text for k in ["calculate", "equation", "math"]):
        return "math"
    return "general"

def choose(mode: str, message: str) -> Route:
    task = classify(message)
    if mode == "council":
        return Route("council", "Multiple specialist responses are requested.")
    if mode == "deep":
        return Route("deep-research", "Deep mode enables multi-stage orchestration.")
    if mode == "fast":
        return Route("fast", "Fast mode prioritizes a single low-latency response.")
    return Route(task, f"Auto-routing classified the task as {task}.")
