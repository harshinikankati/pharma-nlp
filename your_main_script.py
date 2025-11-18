# your_main_script.py

from services.alternatives import get_alternatives

# Example usage:
drug_name = "Aspirin"
alternatives = get_alternatives(drug_name)
print(f"Alternatives for {drug_name}: {alternatives}")
