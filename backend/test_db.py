from google.cloud import datastore

def test_connection():
    print("Testing connection to Firestore in Datastore mode...")
    client = datastore.Client(project='fc-itw-esteban')
    
    try:
        # Try to list the first 1 entities (won't fail even if no entities exist)
        query = client.query(kind='__Stat_Total__')
        entities = list(query.fetch(limit=1))
        print("✅ Successfully connected to Firestore in Datastore mode!")
        print(f"Project ID: fc-itw-esteban")
        print(f"Database ID: (default)")
        return True
    except Exception as e:
        print(f"❌ Failed to connect to Firestore: {str(e)}")
        return False

if __name__ == '__main__':
    test_connection()