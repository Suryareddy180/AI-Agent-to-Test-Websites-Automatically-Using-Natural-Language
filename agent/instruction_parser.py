"""
Instruction Parser Module
Interprets natural language test descriptions and maps them to browser actions.
"""

import re


def parse_instruction(instruction: str) -> list:
    """
    Parse natural language test instruction into structured commands.
    
    Args:
        instruction: Natural language test case description
    
    Returns:
        List of action dictionaries with 'action', 'target', and optional 'value'
    """
    
    original_instruction = instruction
    instruction = instruction.lower()
    actions = []

    # -------- URL EXTRACTION --------
    url_match = re.search(r'https?://[^\s]+', original_instruction)
    extracted_url = url_match.group(0) if url_match else None

    # -------- PAGE NAVIGATION --------
    if "open" in instruction or "navigate" in instruction or "go to" in instruction:
        if extracted_url:
            actions.append({
                "action": "open_page",
                "target": "url",
                "value": extracted_url
            })
        else:
            page = "unknown page"
            
            if "home" in instruction:
                page = "home page"
            elif "login" in instruction:
                page = "login page"
            elif "dashboard" in instruction:
                page = "dashboard page"
            elif "profile" in instruction:
                page = "profile page"
            elif "settings" in instruction:
                page = "settings page"

            actions.append({
                "action": "open_page",
                "target": page
            })

    # -------- TEXT INPUT --------
    if "enter" in instruction or "type" in instruction or "fill" in instruction:
        # Extract value using patterns like 'enter "value"' or 'type value in'
        value_match = re.search(r'["\']([^"\']+)["\']', original_instruction)
        value = value_match.group(1) if value_match else "test_value"
        
        if "username" in instruction:
            actions.append({
                "action": "enter_text",
                "target": "username field",
                "value": value
            })

        if "password" in instruction:
            actions.append({
                "action": "enter_text",
                "target": "password field",
                "value": value
            })

        if "email" in instruction:
            actions.append({
                "action": "enter_text",
                "target": "email field",
                "value": value
            })
            
        if "search" in instruction:
            actions.append({
                "action": "enter_text",
                "target": "search field",
                "value": value
            })

    # -------- CLICK ACTION --------
    if "click" in instruction or "submit" in instruction or "press" in instruction:
        button = "button"

        if "submit" in instruction:
            button = "submit button"
        elif "login" in instruction or "sign in" in instruction:
            button = "login button"
        elif "save" in instruction:
            button = "save button"
        elif "search" in instruction:
            button = "search button"
        elif "register" in instruction or "sign up" in instruction:
            button = "register button"

        actions.append({
            "action": "click",
            "target": button
        })

    # -------- VERIFY/CHECK ACTIONS --------
    if "verify" in instruction or "check" in instruction or "assert" in instruction:
        # Extract what to verify
        if "error" in instruction:
            actions.append({
                "action": "verify",
                "target": "error message"
            })
        elif "success" in instruction:
            actions.append({
                "action": "verify",
                "target": "success message"
            })
        elif "title" in instruction:
            actions.append({
                "action": "verify",
                "target": "page title"
            })
        elif "text" in instruction:
            # Try to extract the text to verify
            text_match = re.search(r'["\']([^"\']+)["\']', original_instruction)
            text = text_match.group(1) if text_match else "expected text"
            actions.append({
                "action": "verify",
                "target": text
            })
        else:
            actions.append({
                "action": "verify",
                "target": "element"
            })

    # -------- WAIT ACTION --------
    if "wait" in instruction:
        seconds_match = re.search(r'(\d+)\s*(?:second|sec|s)', instruction)
        seconds = int(seconds_match.group(1)) if seconds_match else 2
        actions.append({
            "action": "wait",
            "target": "page",
            "value": seconds
        })

    return actions
