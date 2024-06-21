from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, FieldType
from org.apache.lucene.index import IndexWriter, IndexWriterConfig, DirectoryReader
from org.apache.lucene.store import SimpleFSDirectory
from java.nio.file import Paths

import jsonlines

# Function to create Lucene index
def create_index(input_file_path, index_dir):
    analyzer = StandardAnalyzer()
    config = IndexWriterConfig(analyzer)
    
    try:
        directory = SimpleFSDirectory(Paths.get(index_dir))
        writer = IndexWriter(directory, config)
        
        # Open keywords JSONL file for reading
        with jsonlines.open(input_file_path) as reader:
            for obj in reader:
                doc_id = obj['doc_id']
                keywords = obj['keywords']
                
                # Create a Lucene document
                doc = Document()
                doc.add(Field("doc_id", doc_id, FieldType.stored()))
                
                # Add each keyword as a separate field
                for idx, keyword in enumerate(keywords):
                    doc.add(Field(f"keyword_{idx}", keyword, FieldType.stored()))
                
                # Add the document to the index
                writer.addDocument(doc)
        
        # Commit changes and close resources
        writer.commit()
        writer.close()
        directory.close()
        
        print(f"Indexing complete. Indexed {reader.line_num} documents.")
    
    except Exception as e:
        print(f"Error during indexing: {e}")

# Example usage
input_file_path = '/home/shuvam/Information_Retrieval/Corpus_analysis/key.jsonl'
index_dir = '/home/shuvam/Information_Retrieval/Corpus_analysis'

# Create index
create_index(input_file_path, index_dir)
