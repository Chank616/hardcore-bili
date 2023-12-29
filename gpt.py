def send_msg(prompt: str) -> str:
    ls = ["A", "B", "C", "D"]
    return ls[len(prompt) % 4]
