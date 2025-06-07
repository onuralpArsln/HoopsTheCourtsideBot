import pandas as pd
from llm import embeddings  # imports your initialized embeddings from llm.py
from tqdm import tqdm

# Load your CSV
df = pd.read_csv("data/match_summaries.csv")  # replace with your actual filename

# Make sure 'match_summary' exists
if 'summary' not in df.columns:
    raise ValueError("CSV must have a 'summary' column.")

# Generate embeddings
print("Generating embeddings for match summaries...")
summary_texts = df['summary'].fillna("").tolist()

# Optionally show a progress bar
embedding_vectors = []
for summary in tqdm(summary_texts):
    embedding = embeddings.embed_query(summary)
    embedding_vectors.append(embedding)

# Add to DataFrame
df["summary_embedding"] = embedding_vectors

# Save the new DataFrame
output_path = "data/matches_with_embeddings.csv"
df.to_csv(output_path, index=False)

print(f"Saved embedded CSV to: {output_path}")
