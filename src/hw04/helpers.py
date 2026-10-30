from hw04.log import log_action_message


def ask_path(label: str, default: str) -> str:
    return (
        log_action_message(f"Path to the {label} or press 'Enter' for default: ")
        or default
    )
