def parse_instruction(instruction: str):
    """
    Converts natural language instruction into structured actions.
    Milestone-2 logic (rule-based parsing).
    """

    instruction = instruction.lower()
    actions = []

    if "open" in instruction or "navigate" in instruction:
        actions.append({
            "action": "open_page",
            "target": "login page" if "login" in instruction else "home page"
        })

    if "enter" in instruction or "type" in instruction:
        if "username" in instruction:
            actions.append({
                "action": "enter_text",
                "target": "username field"
            })
        if "password" in instruction:
            actions.append({
                "action": "enter_text",
                "target": "password field"
            })

    if "click" in instruction or "submit" in instruction:
        actions.append({
            "action": "click",
            "target": "submit button"
        })

    return actions
