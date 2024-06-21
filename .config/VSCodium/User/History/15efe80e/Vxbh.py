import glob
import os

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
    qrel_path = "/home/shuvam/Codes/Random/qrel.txt"
    results_pattern = "/home/shuvam/Information_Retrieval/reults_bm25/results_k1_*_*_b_#_#_txt"
    output_dir = "/home/shuvam/Codes/Random/output"
    os.makedirs(output_dir, exist_ok=True)

    qrel_dict = parse_qrel(qrel_path)
    mrr_scores = []

    for results_path in glob.glob(results_pattern):
        results_dict = parse_results(results_path)
        filename = os.path.basename(results_path)
        output_filename = filename.replace("results", "ranked_results_mrr")
        output_path = os.path.join(output_dir, output_filename)
        mrr = find_doc_rank(qrel_dict, results_dict, output_path)
        
        # Extract k1 and b values from the filename
        k1_b = filename.split('_')[2:5:2]
        k1 = k1_b[0]
        b = k1_b[1]
        mrr_scores.append((k1, b, mrr))

    # Write all MRR scores to a summary file
    summary_path = os.path.join(output_dir, "mrr_summary.txt")
    with open(summary_path, 'w') as summary_file:
        summary_file.write("k1\tb\tMRR\n")
        for k1, b, mrr in mrr_scores:
            summary_file.write(f"{k1}\t{b}\t{mrr:.4f}\n")

if __name__ == "__main__":
    main()
