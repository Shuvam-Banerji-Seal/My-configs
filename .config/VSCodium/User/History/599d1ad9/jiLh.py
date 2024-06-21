import jsonlines
import string
import re
import spacy
from multiprocessing import Pool, cpu_count, current_process
import nltk
from nltk.corpus import wordnet as wn

# Initialize spaCy with English model
nlp = spacy.load('en_core_web_sm')

# Function to clean and tokenize text using spaCy
def clean_and_tokenize(text):
    # Remove non-ASCII characters and normalize whitespace
    text = re.sub(r'\s+', ' ', text)
    text = text.replace('\n', ' ').replace('\t', ' ')
    
    # Apply spaCy NLP pipeline
    doc = nlp(text)
    
    # Lemmatize tokens, remove stopwords and non-alphabetic tokens
    tokens = [token.lemma_.lower() for token in doc if not token.is_stop and token.is_alpha]
    
    # Remove punctuations and single character tokens
    cleaned_tokens = [token for token in tokens if token not in string.punctuation and len(token) > 1]
    
    # Join tokens to form the cleaned text
    cleaned_text = " ".join(cleaned_tokens)
    
    return cleaned_text

def expand_query(query_text):
    # Simple heuristic for query expansion based on known genres
    genre_keywords = {'action': ['fight', 'battle', 'war', 'combat', 'action', 'adventure', 'hero', 'thrill', 'explosion'],
    'adventure': ['journey', 'explore', 'quest', 'treasure', 'discovery', 'wilderness', 'adventure', 'epic'],
    'animation': ['animated', 'cartoon', 'anime', 'pixar', 'disney', 'cgi', 'animated', 'animation'],
    'comedy': ['funny', 'humor', 'laugh', 'joke', 'comic', 'satire', 'parody', 'comedy', 'hilarious'],
    'crime': ['criminal', 'detective', 'investigation', 'gangster', 'heist', 'mafia', 'crime', 'suspense'],
    'drama': ['love', 'relationship', 'friendship', 'lonely', 'trouble', 'drama', 'heartfelt', 'emotional'],
    'fantasy': ['magic', 'wizard', 'fairy', 'myth', 'legend', 'fantasy', 'enchanted', 'fantastical'],
    'horror': ['scary', 'fear', 'haunted', 'evil', 'dark', 'creepy', 'horror', 'spooky', 'supernatural'],
    'musical': ['music', 'sing', 'dance', 'musical', 'broadway', 'showtunes', 'song', 'performance'],
    'mystery': ['mysterious', 'puzzle', 'detective', 'crime', 'enigma', 'suspense', 'mystery', 'twist'],
    'romance': ['romantic', 'love', 'affection', 'heart', 'couple', 'passion', 'romance', 'sentimental'],
    'sci-fi': ['scifi', 'science', 'futuristic', 'space', 'alien', 'robot', 'cyberpunk', 'sci-fi', 'future'],
    'thriller': ['suspense', 'mystery', 'danger', 'tension', 'action', 'thriller', 'intense', 'nail-biting'],
    'war': ['battlefield', 'war', 'soldier', 'military', 'combat', 'warfare', 'patriotic', 'battle'],
    'western': ['cowboy', 'outlaw', 'sheriff', 'wild west', 'frontier', 'western', 'gunslinger', 'saloon'],
    'biography': ['biopic', 'true story', 'biography', 'historical', 'real life', 'portrait', 'life story'],
    'documentary': ['documentary', 'real footage', 'non-fiction', 'interview', 'archive', 'documentary', 'real'],
    'family': ['family', 'children', 'kids', 'parenting', 'animated', 'family friendly', 'wholesome'],
    'history': ['historical', 'period', 'era', 'history', 'past', 'historian', 'epoch', 'historical'],
    'music': ['music', 'band', 'concert', 'musician', 'rock', 'jazz', 'pop', 'music', 'melody'],
    'sport': ['sports', 'athlete', 'competition', 'championship', 'sporting event', 'fitness', 'athletic'],
    'superhero': ['superhero', 'superpowers', 'cape', 'comic book', 'heroic', 'superhuman', 'superhero'],
    'teen': ['teenager', 'high school', 'coming of age', 'adolescent', 'teen', 'youth', 'teenage'],
    'political': ['politics', 'government', 'political', 'election', 'policy', 'political intrigue', 'political'],
    'psychological': ['psychological', 'mind', 'mental', 'psyche', 'psychiatrist', 'psychological thriller', 'mind game'],
    'noir': ['noir', 'dark', 'shadow', 'mystery', 'detective', 'noir film', 'noir', 'gritty'],
    'romantic comedy': ['romantic comedy', 'romcom', 'romantic', 'comedy', 'funny', 'romantic', 'humorous'],
    'science fiction': ['science fiction', 'scifi', 'futuristic', 'space', 'alien', 'robot', 'sci-fi', 'advanced'],
    'musical drama': ['musical drama', 'music', 'sing', 'dance', 'drama', 'musical', 'emotional', 'performance'],
    'historical drama': ['historical drama', 'history', 'drama', 'period', 'era', 'historical', 'dramatic'],
    'animated fantasy': ['animated fantasy', 'animation', 'cartoon', 'fantasy', 'animated', 'magic', 'enchanted'],
    'crime thriller': ['crime thriller', 'crime', 'thriller', 'suspense', 'detective', 'action-packed', 'intrigue'],
    'biographical drama': ['biographical drama', 'biopic', 'true story', 'drama', 'biography', 'emotional', 'realistic'],
    'horror comedy': ['horror comedy', 'horror', 'comedy', 'funny', 'scary', 'parody', 'dark humor'],
    'war drama': ['war drama', 'war', 'drama', 'soldier', 'military', 'combat', 'intense', 'heroic'],
    'romantic drama': ['romantic drama', 'romance', 'drama', 'love', 'heartfelt', 'emotional', 'intimate'],
    'sci-fi thriller': ['sci-fi thriller', 'science fiction', 'scifi', 'thriller', 'futuristic', 'suspenseful', 'action-packed'],
    'action comedy': ['action comedy', 'action', 'comedy', 'funny', 'humor', 'exciting', 'lighthearted'],
    'fantasy adventure': ['fantasy adventure', 'fantasy', 'adventure', 'quest', 'mythical', 'journey', 'epic'],
    'mystery thriller': ['mystery thriller', 'mystery', 'thriller', 'suspense', 'enigma', 'twist', 'intriguing'],
    'historical epic': ['historical epic', 'historical', 'epic', 'period', 'history', 'majestic', 'grand'],
    'documentary drama': ['documentary drama', 'documentary', 'drama', 'real footage', 'true story', 'insightful', 'provocative'],
    'superhero action': ['superhero action', 'superhero', 'action', 'heroic', 'superhuman', 'exciting', 'powerful']}

    
    expanded_terms = set()
    
    # Tokenize query text
    tokens = query_text.lower().split()
    
    # Expand query based on genre keywords
    for genre, keywords in genre_keywords.items():
        for token in tokens:
            if token in keywords:
                expanded_terms.add(genre)
                break
    
    return list(expanded_terms)

def process_query(query):
    query_id = query['query_id']
    query_text = query['query']
    
    # Clean and tokenize query text
    cleaned_text = clean_and_tokenize(query_text)
    
    # Expand query to infer genre
    inferred_genre = expand_query(query_text)
    
    return {
        'query_id': query_id,
        'query': cleaned_text,
        'Genre': inferred_genre  # Include the inferred genre under 'Genre' field
    }

def process_and_write_query(query, output_file_path):
    try:
        process_id = current_process().name
        print(f"Processing query ID {query['query_id']} on {process_id}")
        processed_query = process_query(query)
        with jsonlines.open(output_file_path, mode='a') as writer:
            writer.write(processed_query)
    except Exception as e:
        print(f"Error processing query ID {query['query_id']}: {e}")

def process_queries(input_file_path, output_file_path):
    # Open the input JSONL file for reading
    with jsonlines.open(input_file_path) as reader:
        # Initialize multiprocessing pool
        pool = Pool(processes=cpu_count())

        try:
            # Process each query individually
            for query in reader:
                pool.apply_async(process_and_write_query, (query, output_file_path))

            pool.close()
            pool.join()

        finally:
            pool.close()
            pool.join()


# Example usage
input_file_path = '/home/shuvam/Information_Retrieval/query_analysis/queries.jsonl'
output_file_path = '/home/shuvam/Information_Retrieval/query_analysis/cleaned_queries.jsonl'
process_queries(input_file_path, output_file_path)
