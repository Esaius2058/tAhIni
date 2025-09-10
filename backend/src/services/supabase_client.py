import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")

if not supabase_key or not supabase_url:
    raise RuntimeError("Supabase credentials are missing")

supabase_client: Client = create_client(supabase_url, supabase_key)
