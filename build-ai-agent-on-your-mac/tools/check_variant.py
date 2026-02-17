check_variant_schema = {
    "type": "function",
    "function": {
        "name": "check_variant",
        "description": "Check if patient has a variant in a specific gene",
        "parameters": {
            "type": "object",
            "properties": {
                "gene": {
                    "type": "string",
                    "description": "Gene symbol (e.g., 'SCN1A', 'BRCA1')"
                }
            },
            "required": ["gene"]
        }
    }
}

def check_variant(gene):
    """
    Check if a patient has a variant in the specified gene.
    Returns variant information if found.
    """
    # Simulated patient variant data
    patient_variants = {
        'SCN1A': 'chr2:166245425:T:C',
        'BRCA1': 'chr17:43094464:G:A',
        'TP53': 'chr17:7675088:C:T'
    }
    
    # Normalize gene symbol
    gene_upper = gene.upper().strip()
    
    # Check for variant
    variant = patient_variants.get(gene_upper)
    
    if variant:
        return {
            "gene": gene_upper,
            "variant_found": True,
            "variant_id": variant,
            "message": f"Patient has variant {variant} in gene {gene_upper}"
        }
    else:
        return {
            "gene": gene_upper,
            "variant_found": False,
            "variant_id": None,
            "message": f"No variant found in gene {gene_upper}"
        }
