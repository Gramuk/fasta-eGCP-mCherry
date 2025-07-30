#!/usr/bin/env python3
"""
FASTA file processor that replaces eGFP sequences with mCherry sequences.

This script reads a FASTA file, combines multi-line sequences into single lines,
performs a sequence substitution (eGFP -> mCherry), and rewraps sequences to
100 characters per line.
"""

import argparse
import re
import sys
from pathlib import Path


def wrap_sequence(sequence, width=80):
    """Wrap a sequence to specified width."""
    return '\n'.join(sequence[i:i+width] for i in range(0, len(sequence), width))


def process_fasta(input_file, output_file):
    """
    Process FASTA file: combine sequences, perform substitution, and rewrap.
    
    Args:
        input_file (str): Path to input FASTA file
        output_file (str): Path to output FASTA file
    """
    # Define the sequences for substitution
    egfp_sequence = "ATGGTGAGCAAGGGCGAGGAGCTGTTCACCGGGGTGGTGCCCATCCTGGTCGAGCTGGACGGCGACGTAAACGGCCACAAGTTCAGCGTGTCCGGCGAGGGCGAGGGCGATGCCACCTACGGCAAGCTGACCCTGAAGTTCATCTGCACCACCGGCAAGCTGCCCGTGCCCTGGCCCACCCTCGTGACCACCCTGACCTACGGCGTGCAGTGCTTCAGCCGCTACCCCGACCACATGAAGCAGCACGACTTCTTCAAGTCCGCCATGCCCGAAGGCTACGTCCAGGAGCGCACCATCTTCTTCAAGGACGACGGCAACTACAAGACCCGCGCCGAGGTGAAGTTCGAGGGCGACACCCTGGTGAACCGCATCGAGCTGAAGGGCATCGACTTCAAGGAGGACGGCAACATCCTGGGGCACAAGCTGGAGTACAACTACAACAGCCACAACGTCTATATCATGGCCGACAAGCAGAAGAACGGCATCAAGGTGAACTTCAAGATCCGCCACAACATCGAGGACGGCAGCGTGCAGCTCGCCGACCACTACCAGCAGAACACCCCCATCGGCGACGGCCCCGTGCTGCTGCCCGACAACCACTACCTGAGCACCCAGTCCGCCCTGAGCAAAGACCCCAACGAGAAGCGCGATCACATGGTCCTGCTGGAGTTCGTGACCGCCGCCGGGATCACTCTCGGCATGGACGAGCTGTACAAG"
    
    mcherry_sequence = "ATGGTGAGCAAGGGCGAGGAGGATAACATGGCCATCATCAAGGAGTTCATGCGCTTCAAGGTGCACATGGAGGGCTCCGTGAACGGCCACGAGTTCGAGATCGAGGGCGAGGGCGAGGGCCGCCCCTACGAGGGCACCCAGACCGCCAAGCTGAAGGTGACCAAGGGTGGCCCCCTGCCCTTCGCCTGGGACATCCTGTCCCCTCAGTTCATGTACGGCTCCAAGGCCTACGTGAAGCACCCCGCCGACATCCCCGACTACTTGAAGCTGTCCTTCCCCGAGGGCTTCAAGTGGGAGCGCGTGATGAACTTCGAGGACGGCGGCGTGGTGACCGTGACCCAGGACTCCTCCCTGCAGGACGGCGAGTTCATCTACAAGGTGAAGCTGCGCGGCACCAACTTCCCCTCCGACGGCCCCGTAATGCAGAAGAAGACCATGGGCTGGGAGGCCTCCTCCGAGCGGATGTACCCCGAGGACGGCGCCCTGAAGGGCGAGATCAAGCAGAGGCTGAAGCTGAAGGACGGCGGCCACTACGACGCTGAGGTCAAGACCACCTACAAGGCCAAGAAGCCCGTGCAGCTGCCCGGCGCCTACAACGTCAACATCAAGTTGGACATCACCTCCCACAACGAGGACTACACCATCGTGGAACAGTACGAACGCGCCGAGGGCCGCCACTCCACCGGCGGCATGGACGAGCTGTACAAG"
    
    print(f"Starting to process {input_file}...")
    
    try:
        with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
            current_header = None
            current_sequence = ""
            sequence_count = 0
            
            print(f"Starting to process {input_file}...")
            
            for line in infile:
                line = line.strip()
                
                if line.startswith('>'):
                    # Process previous sequence if exists
                    if current_header is not None:
                        # Perform sequence substitution
                        current_sequence = current_sequence.replace(egfp_sequence, mcherry_sequence)
                        
                        # Write header
                        outfile.write(current_header + '\n')
                        
                        # Write wrapped sequence
                        if current_sequence:
                            wrapped_sequence = wrap_sequence(current_sequence, 80)
                            outfile.write(wrapped_sequence + '\n')
                        
                        sequence_count += 1
                        
                        # Progress update every 100 sequences
                        if sequence_count % 100 == 0:
                            print(f"Processed {sequence_count} sequences...")
                    
                    # Start new sequence
                    current_header = line
                    current_sequence = ""
                    
                    # Show current header being processed (truncate if too long)
                    header_display = current_header[:60] + "..." if len(current_header) > 60 else current_header
                    print(f"Processing: {header_display}")
                
                elif line:  # Non-empty sequence line
                    current_sequence += line
            
            # Process the last sequence
            if current_header is not None:
                # Perform sequence substitution
                current_sequence = current_sequence.replace(egfp_sequence, mcherry_sequence)
                
                # Write header
                outfile.write(current_header + '\n')
                
                # Write wrapped sequence
                if current_sequence:
                    wrapped_sequence = wrap_sequence(current_sequence, 100)
                    outfile.write(wrapped_sequence + '\n')
                
                sequence_count += 1
        
        print(f"Successfully processed {sequence_count} sequences from {input_file} -> {output_file}")
        
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.", file=sys.stderr)
        sys.exit(1)
    except IOError as e:
        print(f"Error processing files: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    """Main function to handle command line arguments."""
    parser = argparse.ArgumentParser(
        description="Process FASTA files: replace eGFP with mCherry sequences and rewrap to 100 chars per line"
    )
    parser.add_argument(
        "input_file", 
        help="Input FASTA file path"
    )
    parser.add_argument(
        "output_file", 
        help="Output FASTA file path"
    )
    parser.add_argument(
        "-w", "--width", 
        type=int, 
        default=80, 
        help="Sequence line width (default: 60)"
    )
    
    args = parser.parse_args()
    
    # Validate input file exists
    if not Path(args.input_file).exists():
        print(f"Error: Input file '{args.input_file}' does not exist.", file=sys.stderr)
        sys.exit(1)
    
    # Process the file
    process_fasta(args.input_file, args.output_file)


if __name__ == "__main__":
    main()
