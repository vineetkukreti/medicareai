from qdrant_client import QdrantClient
import os

print("Inspecting QdrantClient...")
client = QdrantClient(location=":memory:")
print("Methods:", [m for m in dir(client) if not m.startswith("_")])
