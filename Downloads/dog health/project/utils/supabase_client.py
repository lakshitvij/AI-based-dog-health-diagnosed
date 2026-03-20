import os
from supabase import create_client, Client
SUPABASE_URL = os.getenv("https://oixatobhvywjxjxeaisu.supabase.co")
SUPABASE_KEY = os.getenv("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9peGF0b2JoeXZ3andjeHhlaXN1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzM1NDE5MzEsImV4cCI6MjA4OTExNzkzMX0.2_WvXWbtdNRBoIe9jn92xtLKdmXWVZina_barNV_alY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_supabase_client():
    """Get Supabase client instance"""
    return supabase

def save_prediction(user_id, prediction_data):
    """Save prediction to database"""
    try:
        response = supabase.table('predictions').insert({
            'user_id': user_id,
            'prediction_type': prediction_data.get('type'),
            'input_text': prediction_data.get('input_text'),
            'predicted_disease': prediction_data.get('disease'),
            'confidence': prediction_data.get('confidence'),
            'description': prediction_data.get('description'),
            'severity': prediction_data.get('severity'),
            'care_tips': prediction_data.get('care_tips', []),
            'image_url': prediction_data.get('image_url')
        }).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error saving prediction: {e}")
        return None

def get_user_predictions(user_id, limit=50):
    """Get user's prediction history"""
    try:
        response = supabase.table('predictions').select('*').eq('user_id', user_id).order('created_at', desc=True).limit(limit).execute()
        return response.data
    except Exception as e:
        print(f"Error fetching predictions: {e}")
        return []

def add_favorite(user_id, prediction_id):
    """Add prediction to favorites"""
    try:
        response = supabase.table('favorites').insert({
            'user_id': user_id,
            'prediction_id': prediction_id
        }).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error adding favorite: {e}")
        return None

def remove_favorite(user_id, prediction_id):
    """Remove prediction from favorites"""
    try:
        supabase.table('favorites').delete().eq('user_id', user_id).eq('prediction_id', prediction_id).execute()
        return True
    except Exception as e:
        print(f"Error removing favorite: {e}")
        return False

def get_user_favorites(user_id):
    """Get user's favorite predictions"""
    try:
        response = supabase.table('favorites').select('predictions(*)').eq('user_id', user_id).execute()
        return [fav['predictions'] for fav in response.data if fav['predictions']]
    except Exception as e:
        print(f"Error fetching favorites: {e}")
        return []

def save_user_profile(user_id, profile_data):
    """Create or update user profile"""
    try:
        response = supabase.table('user_profiles').upsert({
            'id': user_id,
            'full_name': profile_data.get('full_name'),
            'avatar_url': profile_data.get('avatar_url'),
            'updated_at': 'now()'
        }).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error saving profile: {e}")
        return None

def get_user_profile(user_id):
    """Get user profile"""
    try:
        response = supabase.table('user_profiles').select('*').eq('id', user_id).maybeSingle().execute()
        return response.data
    except Exception as e:
        print(f"Error fetching profile: {e}")
        return None
