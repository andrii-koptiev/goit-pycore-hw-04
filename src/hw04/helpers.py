from hw04.log import log_prompt


def ask_path(label: str, default: str) -> str:
    return (
        log_prompt(f"Path to the {label} or press 'Enter' for default: ")
        or default
    )
