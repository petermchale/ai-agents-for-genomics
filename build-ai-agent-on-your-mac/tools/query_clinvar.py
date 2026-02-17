query_clinvar_schema = {
    "type": "function",
    "function": {
        "name": "query_clinvar",
        "description": "Check clinical significance of a variant in ClinVar database",
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

def query_clinvar(variant):
    """
    Query ClinVar for clinical significance of a variant.
    Returns clinical interpretation and evidence.
    """
    # Simulated ClinVar data
    clinvar_database = {
        'chr2:166245425:T:C': {
            'significance': 'Pathogenic',
            'review_status': '3-star',
            'condition': 'Dravet syndrome'
        },
        'chr17:43094464:G:A': {
            'significance': 'Likely pathogenic',
            'review_status': '2-star',
            'condition': 'Breast-ovarian cancer, familial'
        },
        'chr17:7675088:C:T': {
            'significance': 'Benign',
            'review_status': '2-star',
            'condition': 'Li-Fraumeni syndrome'
        },
        'chr19:44905796:C:T': {
            'significance': 'Benign/Likely benign',
            'review_status': '2-star',
            'condition': 'not provided'
        }
    }
    
    # Look up variant
    clinvar_entry = clinvar_database.get(variant)
    
    if clinvar_entry:
        return {
            "variant_id": variant,
            "in_clinvar": True,
            "significance": clinvar_entry['significance'],
            "review_status": clinvar_entry['review_status'],
            "condition": clinvar_entry['condition'],
            "interpretation": f"ClinVar: {clinvar_entry['significance']} for {clinvar_entry['condition']}"
        }
    else:
        return {
            "variant_id": variant,
            "in_clinvar": False,
            "significance": "Not in ClinVar",
            "review_status": None,
            "condition": None,
            "interpretation": "Variant not found in ClinVar database"
        }
