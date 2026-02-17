translate_dna_schema = {
    "type": "function",
    "function": {
        "name": "translate_dna",
        "description": "Translate a DNA sequence into its corresponding protein sequence. The DNA sequence should contain only A, T, C, G nucleotides.",
        "parameters": {
            "type": "object",
            "properties": {
                "sequence": {
                    "type": "string",
                    "description": "The DNA sequence to translate (e.g., 'ATGGCCATTGTAATGGGCCGC')"
                }
            },
            "required": ["sequence"]
        }
    }
}

def translate_dna(sequence):
    """
    Translate a DNA sequence to protein.
    Returns the amino acid sequence.
    """
    # Codon to amino acid mapping
    codon_table = {
        'ATA':'I', 'ATC':'I', 'ATT':'I', 'ATG':'M',
        'ACA':'T', 'ACC':'T', 'ACG':'T', 'ACT':'T',
        'AAC':'N', 'AAT':'N', 'AAA':'K', 'AAG':'K',
        'AGC':'S', 'AGT':'S', 'AGA':'R', 'AGG':'R',
        'CTA':'L', 'CTC':'L', 'CTG':'L', 'CTT':'L',
        'CCA':'P', 'CCC':'P', 'CCG':'P', 'CCT':'P',
        'CAC':'H', 'CAT':'H', 'CAA':'Q', 'CAG':'Q',
        'CGA':'R', 'CGC':'R', 'CGG':'R', 'CGT':'R',
        'GTA':'V', 'GTC':'V', 'GTG':'V', 'GTT':'V',
        'GCA':'A', 'GCC':'A', 'GCG':'A', 'GCT':'A',
        'GAC':'D', 'GAT':'D', 'GAA':'E', 'GAG':'E',
        'GGA':'G', 'GGC':'G', 'GGG':'G', 'GGT':'G',
        'TCA':'S', 'TCC':'S', 'TCG':'S', 'TCT':'S',
        'TTC':'F', 'TTT':'F', 'TTA':'L', 'TTG':'L',
        'TAC':'Y', 'TAT':'Y', 'TAA':'*', 'TAG':'*',
        'TGC':'C', 'TGT':'C', 'TGA':'*', 'TGG':'W',
    }
    
    # Clean and uppercase the sequence
    sequence = sequence.upper().replace(" ", "").replace("\n", "")
    
    # Validate DNA sequence
    if not all(base in 'ATCG' for base in sequence):
        return {"error": "Invalid DNA sequence. Only A, T, C, G are allowed."}
    
    # Translate
    protein = []
    for i in range(0, len(sequence) - 2, 3):
        codon = sequence[i:i+3]
        amino_acid = codon_table.get(codon, 'X')  # X for unknown
        if amino_acid == '*':  # Stop codon
            break
        protein.append(amino_acid)
    
    return {
        "dna_sequence": sequence,
        "protein_sequence": ''.join(protein),
        "length": len(protein)
    }
