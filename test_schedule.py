#!/usr/bin/env python3
"""
Test script pour vérifier le traitement des multiples speakers
"""

import json
from schedule import transform_json_to_schedule_format

# Test data avec multiples speakers non-panel
test_data = {
    "schedule": [
        {
            "start": "11:31",
            "end": "11:51",
            "title": "Créer des applications multi-plateformes modernes avec Python et FletX",
            "type": "standard",
            "speaker": [
                {
                    "name": "Wilfrid GOEH",
                    "title": " Créer des applications multi-plateformes modernes avec Python et FletX",
                    "avatar_url": "https://res.cloudinary.com/dvg7vky5o/image/upload/v1751733191/speaker_mal_sahyja.jpg"
                },
                {
                    "name": "Koffi Boris Gilbride WOGLO",
                    "title": "Créer des applications multi-plateformes modernes avec Python et FletX",
                    "avatar_url": "https://res.cloudinary.com/dvg7vky5o/image/upload/v1755133691/boris_hqqfup.jpg"
                }
            ],
            "description": "Dans ce talk, je partagerai mon expérience..."
        },
        {
            "start": "11:51",
            "end": "12:31",
            "title": "Explorer l'impact de Python",
            "type": "panel",
            "description": "Explorer l'impact de Python...",
            "speaker": [
                {
                    "name": "Bassim-Swé Hugues BAMASSI",
                    "title": "Explorer l'impact...",
                    "avatar_url": "https://res.cloudinary.com/dvg7vky5o/image/upload/v1754421104/hugue_d8akpi.jpg"
                },
                {
                    "name": "Pondikpa TCHABAO",
                    "title": "Explorer l'impact...",
                    "avatar_url": "https://res.cloudinary.com/dvg7vky5o/image/upload/v1754849936/tchabao_hokuhh.png"
                }
            ]
        }
    ]
}

def test_multiple_speakers():
    print("Testing multiple speakers handling...")
    
    # Transform the test data
    result = transform_json_to_schedule_format(test_data)
    
    for session in result:
        print(f"\n--- Session: {session['title']} ---")
        print(f"Type: {session['type']}")
        print(f"Speakers: {session['speakers']}")
        print(f"Participant count: {session['participant_count']}")
        print(f"Participant label: {session['participant_label']}")
        print(f"Main avatar: {session.get('avatar_url', 'None')}")
        print(f"All avatars: {session.get('panel_avatars', [])}")
        print(f"Speaker details: {len(session.get('speaker_details', []))} details")
        
        if session.get('speaker_details'):
            for i, detail in enumerate(session['speaker_details']):
                print(f"  Speaker {i+1}: {detail['name']} - {detail.get('avatar_url', 'No avatar')}")

if __name__ == "__main__":
    test_multiple_speakers()
