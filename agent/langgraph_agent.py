from agent.instruction_parser import parse_instruction

def handle_instruction(instruction):
    
    
    parsed_actions = parse_instruction(instruction)

    return {
        "message": "Instruction parsed successfully",
        "parsed_actions": parsed_actions
    }
