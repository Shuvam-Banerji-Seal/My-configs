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
    """Find the rank of the correct document for each query_id and save to a file."""
    with open(output_path, 'w') as out_file:
        for query_id, correct_doc_id in qrel_dict.items():
            if query_id in results_dict:
                try:
                    rank = results_dict[query_id].index(correct_doc_id) + 1
                    out_file.write(f"Query ID: {query_id}, Document ID: {correct_doc_id}, Rank: {rank}\n")
                except ValueError:
                    out_file.write(f"Query ID: {query_id}, Document ID: {correct_doc_id}, Rank: Not found\n")
            else:
                out_file.write(f"Query ID: {query_id} not found in results\n")

if __name__ == "__main__":
    qrel_path = "/home/shuvam/Codes/Random/qrel.txt"
    results_path = "/home/shuvam/Codes/Random/results.txt"
    output_path = "ranked_results.txt"

    qrel_dict = parse_qrel(qrel_path)
    results_dict = parse_results(results_path)

    find_doc_rank(qrel_dict, results_dict, output_path)
