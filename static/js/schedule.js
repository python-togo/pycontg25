/**
 * Schedule Modal Functionality
 * Handles displaying session details in a modal when clicking on session cards
 */

class ScheduleModal {
    constructor() {
        this.modal = null;
        this.sessionData = [];
        this.speakerImages = {};
        this.init();
    }

    init() {
        // Wait for DOM to be fully loaded
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.setup());
        } else {
            this.setup();
        }
    }

    setup() {
        // Get modal element
        this.modal = document.getElementById('session-modal');
        if (!this.modal) {
            console.error('Session modal not found');
            return;
        }

        // Load session data from script tags
        this.loadData();

        // Setup event listeners
        this.setupEventListeners();
    }

    loadData() {
        try {
            // Load session data
            const sessionDataElement = document.getElementById('session-data');
            if (sessionDataElement) {
                this.sessionData = JSON.parse(sessionDataElement.textContent);
            }

            // Load speaker images
            const speakerImagesElement = document.getElementById('speaker-images');
            if (speakerImagesElement) {
                this.speakerImages = JSON.parse(speakerImagesElement.textContent);
            }
        } catch (error) {
            console.error('Error loading session data:', error);
        }
    }

    setupEventListeners() {
        // Add click listeners to all session cards
        const sessionCards = document.querySelectorAll('.session-card[data-session-id]');
        sessionCards.forEach(card => {
            card.addEventListener('click', (e) => {
                const sessionId = card.dataset.sessionId;
                this.openModal(sessionId);
            });

            // Add keyboard support
            card.setAttribute('tabindex', '0');
            card.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    const sessionId = card.dataset.sessionId;
                    this.openModal(sessionId);
                }
            });
        });

        // Close modal event listeners
        const closeButton = this.modal.querySelector('.modal-close');
        if (closeButton) {
            closeButton.addEventListener('click', () => this.closeModal());
        }

        // Close modal when clicking outside
        this.modal.addEventListener('click', (e) => {
            if (e.target === this.modal) {
                this.closeModal();
            }
        });

        // Close modal with Escape key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.modal.style.display !== 'none') {
                this.closeModal();
            }
        });
    }

    openModal(sessionId) {
        const session = this.sessionData.find(s => s.id === sessionId);
        if (!session) {
            console.error('Session not found:', sessionId);
            return;
        }

        this.populateModal(session);
        this.showModal();
    }

    populateModal(session) {
        // Set title
        const titleElement = document.getElementById('modal-title');
        if (titleElement) {
            titleElement.textContent = session.title;
        }

        // Set subtitle
        const subtitleElement = document.getElementById('modal-subtitle');
        if (subtitleElement) {
            if (session.subtitle) {
                subtitleElement.textContent = session.subtitle;
                subtitleElement.style.display = 'block';
            } else {
                subtitleElement.style.display = 'none';
            }
        }

        // Set time
        const timeElement = document.getElementById('modal-time');
        if (timeElement) {
            timeElement.textContent = `${session.start_time} – ${session.end_time}`;
        }

        // Set duration
        const durationElement = document.getElementById('modal-duration');
        if (durationElement) {
            timeElement.textContent = `${session.start_time} – ${session.end_time}`;
        }

        // Set duration
        const diffDurationElement = document.getElementById('modal-duration');
        if (durationElement) {
            durationElement.textContent = `${session.duration} minutes`;
        }

        // Set description
        const descriptionElement = document.getElementById('modal-description');
        if (descriptionElement) {
            descriptionElement.textContent = session.description_full || session.description_short || 'No description available.';
        }

        // Set speakers
        this.populateSpeakers(session);
    }

    populateSpeakers(session) {
        const speakersContainer = document.getElementById('modal-speakers');
        if (!speakersContainer) return;

        if (!session.speakers || session.speakers.length === 0) {
            speakersContainer.style.display = 'none';
            return;
        }

        speakersContainer.style.display = 'block';
        
        // Create speakers section HTML
        const speakersHTML = `
            <h4>${session.participant_label ? session.participant_label.charAt(0).toUpperCase() + session.participant_label.slice(1) : 'Speakers'}</h4>
            <div class="speaker-list">
                ${session.speakers.map((speakerKey, index) => {
                    const imageSrc = this.speakerImages[speakerKey] || '../static/images/speakers/default-avatar.jpg';
                    const speakerName = this.getSpeakerName(speakerKey, index);
                    const speakerTitle = this.getSpeakerTitle(session.participant_label);
                    
                    return `
                        <div class="speaker-item">
                            <img src="${imageSrc}" alt="${speakerName}" class="speaker-avatar" />
                            <div class="speaker-info">
                                <div class="speaker-name">${speakerName}</div>
                                <div class="speaker-title">${speakerTitle}</div>
                            </div>
                        </div>
                    `;
                }).join('')}
            </div>
        `;

        speakersContainer.innerHTML = speakersHTML;
    }

    getSpeakerName(speakerKey, index) {
        // Generate placeholder names based on speaker key
        const names = {
            'speaker1': 'Dr. Kwame Asante',
            'speaker2': 'Sarah Johnson',
            'speaker3': 'Prof. Ama Osei'
        };
        return names[speakerKey] || `Speaker ${index + 1}`;
    }

    getSpeakerTitle(participantLabel) {
        // Generate appropriate titles based on session type
        const titles = {
            'speakers': 'Conference Speaker',
            'instructors': 'Workshop Instructor',
            'experts': 'Technical Expert',
            'panelists': 'Industry Panelist'
        };
        return titles[participantLabel] || 'Python Expert';
    }

    showModal() {
        this.modal.style.display = 'flex';
        // Trigger reflow to ensure display change is registered
        this.modal.offsetHeight;
        this.modal.classList.add('show');
        
        // Focus management for accessibility
        const closeButton = this.modal.querySelector('.modal-close');
        if (closeButton) {
            closeButton.focus();
        }
        
        // Prevent body scroll
        document.body.style.overflow = 'hidden';
    }

    closeModal() {
        this.modal.classList.remove('show');
        
        // Wait for animation to complete before hiding
        setTimeout(() => {
            if (!this.modal.classList.contains('show')) {
                this.modal.style.display = 'none';
            }
        }, 300);
        
        // Restore body scroll
        document.body.style.overflow = '';
    }
}

// Initialize the modal when the script loads
new ScheduleModal();