"""
PyCon Togo 2025 - Schedule Data Handler
Processes JSON schedule data for display
"""

import json
import os
from datetime import datetime

def load_schedule_json():
    """Load schedule data from external JSON file"""
    try:
        # Get the directory of the current script
        current_dir = os.path.dirname(os.path.abspath(__file__))
        json_file_path = os.path.join(current_dir, 'schedule.json')
        
        with open(json_file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Warning: schedule.json not found at {json_file_path}")
        return {"schedule": []}
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return {"schedule": []}
    except Exception as e:
        print(f"Error loading schedule data: {e}")
        return {"schedule": []}

def calculate_duration(start_time, end_time):
    """Calculate duration in minutes from start and end times"""
    try:
        start = datetime.strptime(start_time, "%H:%M")
        end = datetime.strptime(end_time, "%H:%M")
        duration = (end - start).total_seconds() / 60
        return int(duration)
    except:
        return 0

def get_fallback_description(item, description_type='short'):
    """Generate fallback descriptions when not provided in JSON"""
    fallbacks = {
        'talks': {
            'short': f"Session de {len(item.get('talks', []))} présentations techniques",
            'full': f"Cette session comprend {len(item.get('talks', []))} présentations techniques."
        },
        'lightning_talks': {
            'short': f"Présentations rapides de 5 minutes chacune. {len(item.get('talks', []))} talks au programme",
            'full': f"Session de Lightning Talks avec {len(item.get('talks', []))} présentations de 5 minutes."
        },
        'keynote': {
            'short': f"Conférence d'ouverture par {item.get('speaker', 'Invité spécial')}",
            'full': f"Conférence d'ouverture présentée par {item.get('speaker', 'Invité spécial')}."
        },
        'sponsor_session': {
            'short': f"Présentation de nos sponsors et partenaires",
            'full': f"Session dédiée à nos sponsors et partenaires qui soutiennent PyCon Togo 2025."
        },
        'break': {
            'short': f"Temps de pause pour se restaurer et échanger",
            'full': f"Moment convivial pour se détendre et échanger avec les autres participants."
        },
        'opening': {
            'short': f"Ouverture officielle par {item.get('speaker', 'l\'équipe organisatrice')}",
            'full': f"Ouverture officielle de PyCon Togo 2025 par {item.get('speaker', 'l\'équipe organisatrice')}."
        },
        'closing': {
            'short': f"Clôture officielle par {item.get('speaker', 'l\'équipe organisatrice')}",
            'full': f"Clôture officielle de PyCon Togo 2025 par {item.get('speaker', 'l\'équipe organisatrice')}."
        }
    }
    
    session_type = item.get('type', 'session')
    return fallbacks.get(session_type, {}).get(description_type, f"Session {item.get('title', 'sans titre')}")

def transform_json_to_schedule_format(json_data):
    """Transform JSON schedule data to the format expected by the template"""
    schedule_items = []
    
    for item in json_data.get('schedule', []):
        session_id = f"{item['start'].replace(':', '')}-{item.get('type', 'session')}"
        duration = calculate_duration(item['start'], item['end'])
        
        # Determine session type and styling
        if item.get('type') == 'break':
            session_type = 'break'
            participant_count = 0
            speakers = []
            participant_label = ''
        elif item.get('type') in ['opening', 'closing']:
            session_type = 'compact'
            participant_count = 1 if item.get('speaker') else 0
            speakers = [item.get('speaker', '')] if item.get('speaker') else []
            participant_label = 'speaker' if item.get('speaker') else ''
        elif item.get('type') == 'keynote':
            session_type = 'session'
            participant_count = 1
            speakers = [item.get('speaker', 'Keynote Speaker')]
            participant_label = 'speaker'
        elif item.get('type') in ['talks', 'lightning_talks']:
            session_type = 'session'
            talks = item.get('talks', [])
            participant_count = len(talks)
            speakers = [talk.get('speaker', f'Speaker {i+1}') for i, talk in enumerate(talks)]
            participant_label = 'speakers'
        elif item.get('type') == 'sponsor_session':
            session_type = 'session'
            participants = item.get('participants', [])
            participant_count = len(participants)
            speakers = participants
            participant_label = 'participants'
        else:
            session_type = 'session'
            participant_count = 1 if item.get('speaker') else 0
            speakers = [item.get('speaker')] if item.get('speaker') else []
            participant_label = 'speaker'

        # Use JSON description if available, otherwise use fallback
        description_full = item.get('description', get_fallback_description(item, 'full'))
        
        # Create short description (truncate full description or use fallback)
        if item.get('description'):
            # Truncate long descriptions for short version
            description_short = item['description'][:150] + "..." if len(item['description']) > 150 else item['description']
        else:
            description_short = get_fallback_description(item, 'short')

        # For talks sessions, enhance description with talk details if not provided
        if item.get('type') in ['talks', 'lightning_talks'] and not item.get('description'):
            talks_list = item.get('talks', [])
            if talks_list:
                description_short = f"Session de {len(talks_list)} présentations : " + ", ".join([talk['title'][:30] + "..." if len(talk['title']) > 30 else talk['title'] for talk in talks_list[:2]])
                if len(talks_list) > 2:
                    description_short += "..."
                
                description_full = f"Cette session comprend {len(talks_list)} présentations :\n\n" + "\n".join([
                    f"• {talk['title']} par {talk['speaker']} ({talk.get('start', '')}-{talk.get('end', talk.get('duration', ''))})"
                    for talk in talks_list
                ])

        session_data = {
            'id': session_id,
            'title': item.get('title', 'Session sans titre'),
            'subtitle': item.get('subtitle', ''),
            'start_time': item.get('start', ''),
            'end_time': item.get('end', ''), 
            'duration': duration,
            'type': session_type,
            'description_short': description_short,
            'description_full': description_full,
            'speakers': speakers,
            'participant_count': participant_count,
            'participant_label': participant_label,
            'talks': item.get('talks', [])  # Keep original talks data for modal
        }
        
        schedule_items.append(session_data)
    
    return schedule_items

def get_schedule():
    """Return the complete schedule data in the expected format"""
    json_data = load_schedule_json()
    return transform_json_to_schedule_format(json_data)

def get_speaker_images():
    """Return speaker images mapping from avatar URLs in JSON"""
    json_data = load_schedule_json()
    speaker_images = {}
    
    # Extract avatar URLs from JSON data
    for item in json_data.get('schedule', []):
        if 'talks' in item:
            for i, talk in enumerate(item['talks']):
                if talk.get('avatar_url'):
                    # Create unique keys for each speaker
                    speaker_key = f"speaker_{item['start'].replace(':', '')}_{i}"
                    speaker_images[speaker_key] = talk['avatar_url']
        
        # Handle single speaker sessions (keynotes, opening, closing)
        if item.get('speaker') and item.get('avatar_url'):
            speaker_key = f"speaker_{item['start'].replace(':', '')}_main"
            speaker_images[speaker_key] = item['avatar_url']
    
    print(f"Speaker images loaded: {speaker_images}")
    
    return speaker_images

def get_event_info():
    """Return general event information from JSON"""
    json_data = load_schedule_json()
    return {
        'event': json_data.get('event', 'PyCon Togo 2025'),
        'date': json_data.get('date', '2025-08-20'),
        'location': json_data.get('location', 'Lomé, Togo'),
        'timezone': json_data.get('timezone', 'GMT')
    }