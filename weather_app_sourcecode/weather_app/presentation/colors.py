class Colors:
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    RED = "\033[91m"
    RESET = "\033[0m"

    @staticmethod
    def for_temperature(level: str) -> str:
        return {
            "freezing": "blue",
            "cold": "cyan",
            "mild": "green",
            "hot": "red",
        }.get(level, Colors.RESET)
