import os
import json
from collections import Counter
from itertools import combinations

def get_combo_recommendations(current_selection, history_folder="data/sample_bills", top_n=3):
    combo_counter = Counter()

    for filename in os.listdir(history_folder):
        if filename.endswith(".json"):
            with open(os.path.join(history_folder, filename), "r") as f:
                try:
                    bill = json.load(f)
                    items = list(bill.get("items", {}).keys())
                    for combo in combinations(set(items), 2):
                        combo_counter[tuple(sorted(combo))] += 1
                except:
                    continue

    # Find combos that match partially with current selection
    suggestions = []
    for (item1, item2), count in combo_counter.most_common():
        if item1 in current_selection and item2 not in current_selection:
            suggestions.append((item2, count))
        elif item2 in current_selection and item1 not in current_selection:
            suggestions.append((item1, count))

    return sorted(suggestions, key=lambda x: -x[1])[:top_n]
