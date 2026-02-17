analyze_protein_schema = {
    "type": "function",
    "function": {
        "name": "analyze_protein",
        "description": "Analyze a protein sequence to calculate molecular weight, isoelectric point estimate, hydrophobicity, and amino acid composition. Useful for understanding protein properties after translation.",
        "parameters": {
            "type": "object",
            "properties": {
                "sequence": {
                    "type": "string",
                    "description": "The protein sequence to analyze (single-letter amino acid codes, e.g., 'MAIVMGR')"
                }
            },
            "required": ["sequence"]
        }
    }
}

def analyze_protein(sequence):
    """
    Analyze protein sequence properties including molecular weight,
    isoelectric point estimate, and amino acid composition.
    """
    # Molecular weights of amino acids (in Daltons)
    aa_weights = {
        'A': 89.1, 'R': 174.2, 'N': 132.1, 'D': 133.1, 'C': 121.2,
        'Q': 146.2, 'E': 147.1, 'G': 75.1, 'H': 155.2, 'I': 131.2,
        'L': 131.2, 'K': 146.2, 'M': 149.2, 'F': 165.2, 'P': 115.1,
        'S': 105.1, 'T': 119.1, 'W': 204.2, 'Y': 181.2, 'V': 117.1
    }
    
    # pKa values for rough pI estimation
    aa_charge = {
        'D': -1, 'E': -1,  # Acidic
        'K': 1, 'R': 1, 'H': 0.5  # Basic
    }
    
    # Hydrophobicity scale (Kyte-Doolittle)
    hydrophobicity = {
        'I': 4.5, 'V': 4.2, 'L': 3.8, 'F': 2.8, 'C': 2.5,
        'M': 1.9, 'A': 1.8, 'G': -0.4, 'T': -0.7, 'S': -0.8,
        'W': -0.9, 'Y': -1.3, 'P': -1.6, 'H': -3.2, 'E': -3.5,
        'Q': -3.5, 'D': -3.5, 'N': -3.5, 'K': -3.9, 'R': -4.5
    }
    
    sequence = sequence.upper().strip()
    
    # Calculate molecular weight
    mw = sum(aa_weights.get(aa, 0) for aa in sequence)
    # Subtract water for peptide bonds
    mw -= (len(sequence) - 1) * 18.015
    
    # Count amino acids
    aa_composition = {}
    for aa in sequence:
        aa_composition[aa] = aa_composition.get(aa, 0) + 1
    
    # Rough charge estimate
    net_charge = sum(aa_charge.get(aa, 0) for aa in sequence)
    
    # Average hydrophobicity
    avg_hydrophobicity = sum(hydrophobicity.get(aa, 0) for aa in sequence) / len(sequence) if sequence else 0
    
    # Rough pI estimate (simplified)
    acidic_count = aa_composition.get('D', 0) + aa_composition.get('E', 0)
    basic_count = aa_composition.get('K', 0) + aa_composition.get('R', 0) + aa_composition.get('H', 0)
    
    if acidic_count > basic_count:
        pI_estimate = "< 7 (acidic)"
    elif basic_count > acidic_count:
        pI_estimate = "> 7 (basic)"
    else:
        pI_estimate = "~ 7 (neutral)"
    
    return {
        "protein_sequence": sequence,
        "length": len(sequence),
        "molecular_weight_da": round(mw, 2),
        "net_charge": round(net_charge, 1),
        "pI_estimate": pI_estimate,
        "avg_hydrophobicity": round(avg_hydrophobicity, 2),
        "hydrophobicity_classification": "hydrophobic" if avg_hydrophobicity > 0 else "hydrophilic",
        "amino_acid_composition": aa_composition
    }
