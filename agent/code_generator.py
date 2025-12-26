"""
Code Generator Module
Converts parsed actions into executable Playwright Python scripts.
"""

def generate_playwright_code(parsed_actions: list, target_url: str = "http://localhost:5000") -> str:
    """
    Generate Playwright Python script from parsed actions.
    
    Args:
        parsed_actions: List of action dictionaries from instruction parser
        target_url: Base URL for the test
    
    Returns:
        String containing executable Playwright Python code
    """
    
    # Build the Playwright script
    code_lines = [
        "from playwright.sync_api import sync_playwright",
        "",
        "def run_test():",
        "    with sync_playwright() as p:",
        "        browser = p.chromium.launch(headless=True)",
        "        page = browser.new_page()",
        ""
    ]
    
    # Add action-specific code
    for action in parsed_actions:
        action_type = action.get("action")
        target = action.get("target", "")
        value = action.get("value", "")
        
        if action_type == "open_page":
            url = _get_url_for_page(target, target_url)
            code_lines.append(f'        page.goto("{url}")')
            code_lines.append(f'        print("Navigated to: {url}")')
            
        elif action_type == "enter_text":
            selector = _get_selector_for_field(target)
            code_lines.append(f'        page.fill("{selector}", "{value}")')
            code_lines.append(f'        print("Entered text in: {target}")')
            
        elif action_type == "click":
            selector = _get_selector_for_button(target)
            code_lines.append(f'        page.click("{selector}")')
            code_lines.append(f'        print("Clicked: {target}")')
            
        elif action_type == "verify":
            selector = _get_selector_for_element(target)
            code_lines.append(f'        assert page.locator("{selector}").is_visible()')
            code_lines.append(f'        print("Verified: {target} is visible")')
    
    # Close browser and add run block
    code_lines.extend([
        "",
        "        browser.close()",
        '        print("Test completed successfully!")',
        "",
        'if __name__ == "__main__":',
        "    run_test()"
    ])
    
    return "\n".join(code_lines)


def _get_url_for_page(page_name: str, base_url: str) -> str:
    """Map page name to URL path."""
    page_routes = {
        "home page": "/",
        "dashboard page": "/dashboard",
        "profile page": "/profile",
        "settings page": "/settings",
        "login page": "/login",
        "unknown page": "/"
    }
    path = page_routes.get(page_name, "/")
    return f"{base_url}{path}"


def _get_selector_for_field(field_name: str) -> str:
    """Map field name to CSS selector."""
    field_selectors = {
        "username field": 'input[name="username"], input[id="username"], input[placeholder*="username" i]',
        "password field": 'input[type="password"], input[name="password"], input[id="password"]',
        "email field": 'input[type="email"], input[name="email"], input[id="email"]'
    }
    return field_selectors.get(field_name, f'input[name="{field_name}"]')


def _get_selector_for_button(button_name: str) -> str:
    """Map button name to CSS selector."""
    button_selectors = {
        "submit button": 'button[type="submit"], input[type="submit"]',
        "login button": 'button:has-text("Login"), button:has-text("Sign in")',
        "save button": 'button:has-text("Save")',
        "button": "button"
    }
    return button_selectors.get(button_name, f'button:has-text("{button_name}")')


def _get_selector_for_element(element_name: str) -> str:
    """Map element description to CSS selector."""
    return f'text="{element_name}"'


def generate_assertions(parsed_actions: list) -> list:
    """
    Generate assertion statements based on parsed actions.
    
    Args:
        parsed_actions: List of action dictionaries
    
    Returns:
        List of assertion dictionaries
    """
    assertions = []
    
    for action in parsed_actions:
        action_type = action.get("action")
        target = action.get("target", "")
        
        if action_type == "open_page":
            assertions.append({
                "type": "page_loaded",
                "description": f"Page '{target}' should load successfully",
                "check": "page.url contains expected path"
            })
        elif action_type == "click":
            assertions.append({
                "type": "element_clickable",
                "description": f"'{target}' should be clickable",
                "check": "element is visible and enabled"
            })
        elif action_type == "verify":
            assertions.append({
                "type": "element_visible",
                "description": f"'{target}' should be visible",
                "check": "element is present in DOM"
            })
    
    return assertions
