import os
import re

def parse_qrel(qrel_path):
    """Parse qrel file and return a dictionary with query_id as key and doc_id as value."""
    qrel_dict = {}
    with open(qrel_path, 'r') as file:
        for line in file:
            parts = line.strip().split()
            query_id = parts[0]
            doc_id = parts[2]
            qrel_dict[query_id] = doc_id
    return qrel_dict

def parse_results(results_path):
    """Parse results file and return a dictionary with query_id as key and list of doc_ids as value."""
    results_dict = {}
    with open(results_path, 'r') as file:
        current_query_id = None
        for line in file:
            line = line.strip()
            if line.startswith("Query ID:"):
                current_query_id = line.split()[-1]
                results_dict[current_query_id] = []
            elif line.startswith("Total number of matching documents:"):
                continue
            else:
                results_dict[current_query_id].append(line)
    return results_dict

def find_doc_rank(qrel_dict, results_dict, output_path):
    """Find the rank of the correct document for each query_id and save to a file, also calculate MRR."""
    reciprocal_ranks = []
    with open(output_path, 'w') as out_file:
        for query_id, correct_doc_id in qrel_dict.items():
            if query_id in results_dict:
                try:
                    rank = results_dict[query_id].index(correct_doc_id) + 1
                    reciprocal_ranks.append(1 / rank)
                    out_file.write(f"Query ID: {query_id}, Document ID: {correct_doc_id}, Rank: {rank}\n")
                except ValueError:
                    reciprocal_ranks.append(0)
                    out_file.write(f"Query ID: {query_id}, Document ID: {correct_doc_id}, Rank: Not found\n")
            else:
                reciprocal_ranks.append(0)
                out_file.write(f"Query ID: {query_id} not found in results\n")

        # Calculate Mean Reciprocal Rank (MRR)
        if reciprocal_ranks:
            mrr = sum(reciprocal_ranks) / len(reciprocal_ranks)
        else:
            mrr = 0
        out_file.write(f"\nMean Reciprocal Rank (MRR): {mrr:.4f}\n")
    return mrr

def main():
    qrel_path = "/home/shuvam/Information_Retrieval/reults_bm25/qrel_querries/qrel.txt"
    results_dir = "/home/shuvam/Information_Retrieval/reults_bm25/results"
    summary_output_path = "/home/shuvam/Information_Retrieval/reults_bm25/output"
    
    print("Parsing qrel file...")
    qrel_dict = parse_qrel(qrel_path)
    print("Qrel file parsed.")
    
    summary_data = []
    
    # Correcting the regex to match the given format
    results_files = [f for f in os.listdir(results_dir) if re.match(r'results_k1_\d_\d_b_\d_\d_txt', f)]
    
    print(f"Found {len(results_files)} results files.")
    
    for results_file in results_files:
        print(f"Processing file: {results_file}")
        results_path = os.path.join(results_dir, results_file)
        results_dict = parse_results(results_path)
        
        # Extract k1 and b values using the corrected regex pattern
        match = re.match(r'results_k1_(\d_\d)_b_(\d_\d)_txt', results_file)
        
        if match:
            k1_value = match.group(1).replace('_', '.')
            b_value = match.group(2).replace('_', '.')
        
            output_filename = f"ranked_results_mrr_k1_{k1_value.replace('.', '_')}_b_{b_value.replace('.', '_')}.txt"
            output_path = os.path.join(results_dir, output_filename)
        
            print(f"Finding doc rank for k1={k1_value}, b={b_value}")
            mrr = find_doc_rank(qrel_dict, results_dict, output_path)
            print(f"Computed MRR: {mrr} for k1={k1_value}, b={b_value}")
        
            summary_data.append((k1_value, b_value, mrr))
        else:
            print(f"Skipping file {results_file} due to incorrect naming format.")
    
    print("Writing summary file...")
    with open(summary_output_path, 'w') as summary_file:
        for k1, b, mrr in summary_data:
            summary_file.write(f"k1: {k1}, b: {b}, MRR: {mrr:.4f}\n")
    print("Summary file written.")

if __name__ == "__main__":
    main()
