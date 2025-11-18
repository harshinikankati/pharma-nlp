# app.py

from services.alternatives import get_alternatives

# Example usage:
drug_name = "Aspirin"
alternatives = get_alternatives(drug_name)

if alternatives:
    print(f"Alternatives for {drug_name}: {', '.join(alternatives)}")
else:
    print(f"No alternatives found for {drug_name}.")
