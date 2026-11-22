CATEGORIES = ["food", "transport", "housing", "entertainment", "health", "other"]


def normalize_category(name):
    n = name.strip().lower()
    if n in ("food", "groceries", "restaurant", "cafe"):
        return "food"
    elif n in ("transport", "bus", "taxi", "metro"):
        return "transport"
    elif n in ("housing", "rent", "utilities"):
        return "housing"
    elif n in ("entertainment", "cinema", "games"):
        return "entertainment"
    elif n in ("health", "pharmacy", "doctor"):
        return "health"
    else:
        return "other"
