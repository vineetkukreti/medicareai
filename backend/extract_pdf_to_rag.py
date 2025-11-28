"""
Extract text from PDF and update via API
"""
import PyPDF2
import requests

# File details
USER_ID = 3
RECORD_ID = 2
PDF_PATH = "uploads/health_records/3_20251127_175515_Mr. VINEET KUKRETI.pdf"
BASE_URL = "http://localhost:8000"

def extract_pdf_text(pdf_path):
    """Extract text from PDF file"""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text.strip()
    except Exception as e:
        print(f"Error extracting PDF text: {e}")
        return None

def main():
    print(f"Extracting text from PDF: {PDF_PATH}")
    
    # Extract text
    text = extract_pdf_text(PDF_PATH)
    if not text:
        print("❌ Failed to extract text from PDF")
        return
    
    print(f"✅ Extracted {len(text)} characters from PDF")
    print("\nFirst 500 characters:")
    print("="*60)
    print(text[:500])
    print("="*60)
    
    # First refresh embeddings to ensure the record with full text gets indexed
    print("\n🔄 Refreshing embeddings via API...")
    response = requests.post(f"{BASE_URL}/api/insights/refresh?user_id={USER_ID}")
    if response.status_code == 200:
        print("✅ Refresh started")
    
    # Now query with the lab results question
    import time
    time.sleep(3)  # Wait for refresh
    
    print("\n🔍 Testing query: 'What are my lab results?'")
    response = requests.post(
        f"{BASE_URL}/api/insights/query?user_id={USER_ID}",
        json={"query": "What are my lab results? Give me specific values."},
        headers={"Content-Type": "application/json"}
    )
    
    if response.status_code == 200:
        print("\n" + "="*60)
        print("RAG Response:")
        print("="*60)
        print(response.json()['insight'])
    else:
        print(f"❌ Query failed: {response.status_code}")

if __name__ == "__main__":
    main()
