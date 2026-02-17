check_population_frequency_schema = {
    "type": "function",
    "function": {
        "name": "check_population_frequency",
        "description": "Check allele frequency of a variant in gnomAD population database",
        "parameters": {
            "type": "object",
            "properties": {
                "variant": {
                    "type": "string",
                    "description": "Variant ID (e.g., 'chr2:166245425:T:C')"
                }
            },
            "required": ["variant"]
        }
    }
}

def check_population_frequency(variant):
    """
    Check the allele frequency of a variant in population databases.
    Returns frequency and rarity classification.
    """
    # Simulated gnomAD frequency data
    frequency_database = {
        'chr2:166245425:T:C': 0.00001,
        'chr17:43094464:G:A': 0.0002,
        'chr17:7675088:C:T': 0.15,
        'chr19:44905796:C:T': 0.25
    }
    
    # Look up frequency
    frequency = frequency_database.get(variant, 0.0)
    
    # Classify rarity
    if frequency == 0.0:
        classification = "not found in database"
        rarity = "unknown"
    elif frequency < 0.0001:
        classification = "ultra-rare"
        rarity = "very rare"
    elif frequency < 0.01:
        classification = "rare"
        rarity = "rare"
    else:
        classification = "common"
        rarity = "common"
    
    return {
        "variant_id": variant,
        "frequency": frequency,
        "classification": classification,
        "rarity": rarity,
        "interpretation": f"Variant has allele frequency of {frequency} ({rarity})"
    }
