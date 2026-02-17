search_disease_genes_schema = {
    "type": "function",
    "function": {
        "name": "search_disease_genes",
        "description": "Search for genes associated with a disease",
        "parameters": {
            "type": "object",
            "properties": {
                "disease": {
                    "type": "string",
                    "description": "Disease name (e.g., 'epilepsy', 'cancer')"
                }
            },
            "required": ["disease"]
        }
    }
}

def search_disease_genes(disease):
    """
    Search for genes associated with a disease.
    Returns a list of gene symbols.
    """
    # Simulated gene-disease database
    gene_database = {
        'epilepsy': ['SCN1A', 'KCNQ2'],
        'cancer': ['TP53', 'BRCA1', 'BRCA2'],
        'diabetes': ['INS', 'GCK', 'HNF1A'],
        'alzheimer': ['APP', 'PSEN1', 'PSEN2', 'APOE']
    }
    
    # Normalize disease name
    disease_lower = disease.lower().strip()
    
    # Search for genes
    genes = gene_database.get(disease_lower, [])
    
    if not genes:
        return {
            "disease": disease,
            "genes": [],
            "message": f"No known genes found for '{disease}'"
        }
    
    return {
        "disease": disease,
        "genes": genes,
        "count": len(genes)
    }
