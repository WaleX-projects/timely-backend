import chromadb
import numpy as np

# 1. Setup Client and Collection
# Changed name to 'student_faces_v2' to avoid the 1434 dimension error
client = chromadb.PersistentClient(path="./envo_db")

collection = client.get_or_create_collection(
    name="student_faces_v3", 
    metadata={"hnsw:space": "cosine"} 
)

def add_face_to_db(user_id, name, embedding):
    """
    Directly adds the 512-d InsightFace embedding to ChromaDB.
    'embedding' should be a list of 512 floats.
    """
    # NO normalization needed for InsightFace. 
    # Just ensure it is a list.
    if isinstance(embedding, np.ndarray):
        embedding = embedding.tolist()
    
    collection.add(
        embeddings=[embedding],
        metadatas=[{"name": name}],
        ids=[str(user_id)]
    )
    return {"status": "success", "message": f"Successfully enrolled {name}!"}

def search_face(face_embedding):
    """
    Searches for the closest 512-d vector in the DB.
    """
    if isinstance(face_embedding, np.ndarray):
        face_embedding = face_embedding.tolist()

    results = collection.query(
        query_embeddings=[face_embedding],
        n_results=1
    )
    
    if results['ids'] and len(results['ids'][0]) > 0:
        # results['distances'][0][0] is the cosine distance.
        # 0.0 means identical, 1.0+ means very different.
        print(results)
        return results['ids'][0][0], results['distances'][0][0]
    
    return None, 1.0