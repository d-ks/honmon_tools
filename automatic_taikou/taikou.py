def align_two_sequences(seq1, seq2):
    n = len(seq1)
    m = len(seq2)
    # Initialize the scoring matrix with high values
    score = [[float('inf')] * (m + 1) for _ in range(n + 1)]
    traceback = [[None] * (m + 1) for _ in range(n + 1)]
    gap_penalty = 1

    # Set the starting point
    score[0][0] = 0

    # Initialize first column and first row
    for i in range(1, n + 1):
        score[i][0] = score[i - 1][0] + gap_penalty
        traceback[i][0] = 'up'
    for j in range(1, m + 1):
        score[0][j] = score[0][j - 1] + gap_penalty
        traceback[0][j] = 'left'

    # Fill in the scoring and traceback matrices
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if seq1[i - 1] == seq2[j - 1]:
                match = score[i - 1][j - 1]
            else:
                match = float('inf')  # Disallow mismatches
            delete = score[i - 1][j] + gap_penalty  # Gap in seq2
            insert = score[i][j - 1] + gap_penalty  # Gap in seq1
            min_score = min(match, delete, insert)
            score[i][j] = min_score
            if min_score == match:
                traceback[i][j] = 'diag'
            elif min_score == delete:
                traceback[i][j] = 'up'
            else:
                traceback[i][j] = 'left'

    # Traceback to get the alignment
    aligned_seq1 = []
    aligned_seq2 = []
    i, j = n, m
    while i > 0 or j > 0:
        if i > 0 and j > 0 and traceback[i][j] == 'diag':
            aligned_seq1.insert(0, seq1[i - 1])
            aligned_seq2.insert(0, seq2[j - 1])
            i -= 1
            j -= 1
        elif i > 0 and traceback[i][j] == 'up':
            aligned_seq1.insert(0, seq1[i - 1])
            aligned_seq2.insert(0, '・')  # Gap in seq2
            i -= 1
        elif j > 0 and traceback[i][j] == 'left':
            aligned_seq1.insert(0, '・')  # Gap in seq1
            aligned_seq2.insert(0, seq2[j - 1])
            j -= 1
        else:
            break
    return aligned_seq1, aligned_seq2

def align_sequences(sequences):
    # Start with the first sequence as the initial alignment
    alignment = [list(sequences[0])]
    # Align each subsequent sequence to the current alignment
    for seq in sequences[1:]:
        # Build a consensus sequence from the alignment
        consensus = []
        for i in range(len(alignment[0])):
            chars = set(aln_seq[i] for aln_seq in alignment)
            chars.discard('・')
            consensus.append(chars.pop() if chars else '・')
        # Align the consensus sequence with the new sequence
        aligned_consensus, aligned_seq = align_two_sequences(consensus, list(seq))
        # Update the alignment sequences to include any gaps introduced
        new_alignment = []
        for aln_seq in alignment:
            new_aln_seq = []
            idx_aln = 0
            for c in aligned_consensus:
                if c == '・':
                    new_aln_seq.append('・')
                else:
                    new_aln_seq.append(aln_seq[idx_aln])
                    idx_aln += 1
            new_alignment.append(new_aln_seq)
        # Add the new aligned sequence
        new_alignment.append(aligned_seq)
        alignment = new_alignment
    # Convert alignment lists back to strings
    aligned_strings = [''.join(aln_seq) for aln_seq in alignment]
    return aligned_strings

def split_aligned_sequences(aligned_strings, n_length):
    sequences_chunks = []
    for seq in aligned_strings:
        chunks = [seq[i:i+n_length] for i in range(0, len(seq), n_length)]
        sequences_chunks.append(chunks)
    return sequences_chunks

# Example usage:
sequences = [
    "いまはむかしたけとりのおきなといふものありけり野山なるたけをとりてよろつの事につかひけり名をはさるきのみやつこといひける",
    "いまはむかし竹とりのおきなといふものありけり野山にましりて竹をとりつゝよろつの事につかひけり名をはさかきのみやつことなんいひける",
    "いまはむかし竹とりのおきなといふもの有けり野山にましりてたけをとりつゝよろつの事につかひけり名をはさかきのみやつことなむいひける"
]
alignment = align_sequences(sequences)

# Now, split the aligned sequences into chunks of n_length
n_length = 20  # You can adjust this value as needed
sequences_chunks = split_aligned_sequences(alignment, n_length)

# Determine the maximum number of lines
max_lines = max(len(chunks) for chunks in sequences_chunks)

# Print the aligned sequences line by line
num_sequences = len(sequences)
for line_index in range(max_lines):
    for seq_index in range(num_sequences):
        chunks = sequences_chunks[seq_index]
        if line_index < len(chunks):
            line = chunks[line_index]
        else:
            line = ''  # If this sequence doesn't have this line
        print(f"{seq_index+1}: {line}")
    print()  # Print a blank line between groups
