import jsonlines

def count_na_genres(jsonl_file):
    total_queries = 0
    na_genre_count = 0
    
    with jsonlines.open(jsonl_file) as reader:
        for query in reader:
            total_queries += 1
            if query['genre'] == 'N/A':
                na_genre_count += 1
    
    return na_genre_count, total_queries

# Path to your processed queries JSONL file
processed_queries_file = 'processed_queries.jsonl'

# Counting N/A genres
na_count, total_count = count_na_genres(processed_queries_file)

print(f"Total queries: {total_count}")
print(f"Queries with genre as N/A: {na_count}")
print(f"Percentage of queries with genre as N/A: {(na_count / total_count) * 100:.2f}%")
