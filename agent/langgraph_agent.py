def handle_instruction(instruction):
    if not instruction:
        return {
            "message": "No instruction received"
        }

    return {
        "message": "Instruction received successfully",
        "received_instruction": instruction
    }
