from hw04.log import log_goodbye
from hw04.user_menu import main

if __name__ == "__main__":
    try:
        main()

    except (KeyboardInterrupt, EOFError):
        log_goodbye()
