"""
PyCon Togo 2025 - Schedule Data
Contains all session information for the conference schedule
"""

# Speaker images mapping
SPEAKER_IMAGES = {
    'speaker1': '../static/images/speakers/speaker2.jpg',
    'speaker2': '../static/images/speakers/speaker_mal.jpg',
    'speaker3': '../static/images/speakers/speakfemale.jpg',
}

# Schedule data for PyCon Togo 2025
SCHEDULE_DATA = [
    {
        'id': 'registration',
        'title': 'Registration',
        'subtitle': '',
        'start_time': '08:00',
        'end_time': '08:30',
        'duration': 30,
        'type': 'break',
        'description_short': 'Time to check in, grab your badge, and get ready for an exciting day!',
        'description_full': 'Welcome to PyCon Togo 2025! Please arrive early to collect your conference badge, welcome kit, and network with fellow attendees. Our registration desk will be open with friendly volunteers to help you get oriented.',
        'speakers': [],
        'participant_count': 0
    },
    {
        'id': 'welcome_speech',
        'title': 'Welcome Speech',
        'subtitle': '',
        'start_time': '08:30',
        'end_time': '09:00',
        'duration': 30,
        'type': 'compact',
        'description_short': 'Kick off the conference with our organizers and special guests.',
        'description_full': 'Join us for the official opening of PyCon Togo 2025 as our organizers and distinguished guests welcome attendees and set the stage for an incredible day of learning, networking, and Python celebration.',
        'speakers': [],
        'participant_count': 0
    },
    {
        'id': 'opening_keynote',
        'title': 'Opening Keynote',
        'subtitle': "Python's Evolution: From Scripting to AI Powerhouse",
        'start_time': '09:00',
        'end_time': '10:00',
        'duration': 60,
        'type': 'session',
        'description_short': 'Join us for an inspiring journey through Python\'s remarkable transformation from a simple scripting language to the backbone of modern AI and machine learning. Our keynote speakers will explore how Python\'s simplicity and versatility have made it the language of choice for data scientists...',
        'description_full': 'Join us for an inspiring journey through Python\'s remarkable transformation from a simple scripting language to the backbone of modern AI and machine learning. Our keynote speakers will explore how Python\'s simplicity and versatility have made it the language of choice for data scientists, web developers, and AI researchers worldwide. Discover the latest developments in Python 3.12+, upcoming features, and how the Python community continues to drive innovation in technology across Africa and beyond.',
        'speakers': ['speaker1', 'speaker2', 'speaker3'],
        'participant_count': 3,
        'participant_label': 'speakers'
    },
    {
        'id': 'ml_workshop',
        'title': 'Machine Learning Workshop',
        'subtitle': 'Building Intelligent Applications with scikit-learn and TensorFlow',
        'start_time': '10:15',
        'end_time': '12:00',
        'duration': 105,
        'type': 'session',
        'description_short': 'Dive deep into the world of machine learning with Python in this comprehensive hands-on workshop. Learn to build, train, and deploy machine learning models using industry-standard libraries like scikit-learn, pandas, and TensorFlow...',
        'description_full': 'Dive deep into the world of machine learning with Python in this comprehensive hands-on workshop. Learn to build, train, and deploy machine learning models using industry-standard libraries like scikit-learn, pandas, and TensorFlow. We\'ll start with data preprocessing and exploration using pandas and NumPy, then move on to implementing classification and regression models. The workshop includes real-world datasets, feature engineering techniques, model evaluation strategies, and an introduction to neural networks with TensorFlow. Perfect for developers looking to add ML capabilities to their applications or transition into data science roles.',
        'speakers': ['speaker1', 'speaker2', 'speaker3', 'speaker1'],
        'participant_count': 4,
        'participant_label': 'instructors'
    },
    {
        'id': 'lightning_talks',
        'title': 'Lightning Talks',
        'subtitle': '',
        'start_time': '13:00',
        'end_time': '14:00',
        'duration': 60,
        'type': 'session',
        'description_short': 'Rapid-fire community presentations (5 min each). Experience the energy of our Python community as developers, students, and professionals share their projects, insights, and discoveries...',
        'description_full': 'Rapid-fire community presentations (5 min each). Experience the energy of our Python community as developers, students, and professionals share their projects, insights, and discoveries in quick, impactful presentations.',
        'speakers': ['speaker1', 'speaker2', 'speaker3', 'speaker1', 'speaker2'],
        'participant_count': 5,
        'participant_label': 'speakers'
    },
    {
        'id': 'lunch_break',
        'title': 'Lunch Break',
        'subtitle': '',
        'start_time': '14:00',
        'end_time': '15:00',
        'duration': 60,
        'type': 'break',
        'description_short': 'Time to recharge and network with fellow Pythonistas!',
        'description_full': 'Take a break from all the learning and enjoy a delicious lunch while networking with fellow Python enthusiasts. This is a great opportunity to discuss what you\'ve learned so far and make new connections in the Python community.',
        'speakers': [],
        'participant_count': 0
    },
    {
        'id': 'web_workshop',
        'title': 'Modern Web Development Workshop',
        'subtitle': 'Building Scalable APIs with FastAPI and Async Python',
        'start_time': '15:00',
        'end_time': '16:30',
        'duration': 90,
        'type': 'session',
        'description_short': 'Master the art of building high-performance, scalable web APIs using FastAPI and Python\'s async capabilities. This intensive workshop covers async/await patterns, concurrent programming with asyncio...',
        'description_full': 'Master the art of building high-performance, scalable web APIs using FastAPI and Python\'s async capabilities. This intensive workshop covers async/await patterns, concurrent programming with asyncio, and building production-ready REST APIs. You\'ll learn to implement authentication, database integration with async ORMs like SQLAlchemy, request validation with Pydantic models, and API documentation generation. We\'ll also explore deployment strategies, testing async code, and performance optimization techniques. By the end, you\'ll have built a complete async API ready for production deployment with proper error handling and monitoring.',
        'speakers': ['speaker2', 'speaker3', 'speaker1'],
        'participant_count': 3,
        'participant_label': 'experts'
    },
    {
        'id': 'closing_panel',
        'title': 'Closing Panel',
        'subtitle': 'Python in Industry',
        'start_time': '17:00',
        'end_time': '18:00',
        'duration': 60,
        'type': 'session',
        'description_short': 'Discussion with professionals on real-world Python use cases. Join industry leaders as they share insights on how Python is transforming businesses across different sectors...',
        'description_full': 'Discussion with professionals on real-world Python use cases. Join industry leaders as they share insights on how Python is transforming businesses across different sectors, from fintech and healthcare to agriculture and education, with special focus on opportunities in the African tech ecosystem.',
        'speakers': ['speaker2', 'speaker3', 'speaker1', 'speaker2'],
        'participant_count': 4,
        'participant_label': 'panelists'
    }
]

def get_schedule():
    """Return the complete schedule data"""
    return SCHEDULE_DATA

def get_session_by_id(session_id):
    """Get a specific session by its ID"""
    for session in SCHEDULE_DATA:
        if session['id'] == session_id:
            return session
    return None

def get_sessions_by_type(session_type):
    """Get all sessions of a specific type (session, break, compact)"""
    return [session for session in SCHEDULE_DATA if session['type'] == session_type]