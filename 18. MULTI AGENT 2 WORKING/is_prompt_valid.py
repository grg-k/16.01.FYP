# to ignore replies that are toolcalls or apologies
def is_reply_valid(answer: str) -> bool:
    if not answer or not answer.strip():
        return False
    low = answer.lower()
    if "sorry" in low and len(answer) < 60:
        return False
    if '"tool_name":' in answer or "[TOOL]" in answer:
        return False
    return True