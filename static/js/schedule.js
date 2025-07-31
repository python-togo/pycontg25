/**
 * Schedule Modal Functionality - Updated for individual talk sessions
 * Handles displaying session details in a modal when clicking on session cards
 */

class ScheduleModal {
    constructor() {
        this.modal = null;
        this.sessionData = [];
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
            durationElement.textContent = `${session.duration} minutes`;
        }

        // Set description
        const descriptionElement = document.getElementById('modal-description');
        if (descriptionElement) {
            // Handle line breaks in description
            const description = session.description_full || session.description_short || 'Aucune description disponible.';
            descriptionElement.innerHTML = description.replace(/\n/g, '<br>');
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
        const participantLabel = this.getParticipantLabel(session.participant_label, session.speakers.length);
        
        const speakersHTML = `
            <h4>${participantLabel}</h4>
            <div class="speaker-list">
                ${session.speakers.map((speaker, index) => {
                    let avatarSrc = '../static/images/speakers/default-avatar.jpg';
                    
                    // Try to get avatar from talks data
                    if (session.talks && session.talks[index] && session.talks[index].avatar_url) {
                        avatarSrc = session.talks[index].avatar_url;
                    }
                    
                    const speakerTitle = this.getSpeakerTitle(session.participant_label);
                    
                    return `
                        <div class="speaker-item">
                            <img src="${avatarSrc}" alt="${speaker}" class="speaker-avatar" 
                                 onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';" />
                            <div class="speaker-avatar" style="display: none; background: #004225; color: white; align-items: center; justify-content: center; font-weight: bold; font-size: 1rem;">
                                ${speaker.charAt(0)}
                            </div>
                            <div class="speaker-info">
                                <div class="speaker-name">${speaker}</div>
                                <div class="speaker-title">${speakerTitle}</div>
                                ${session.talks && session.talks[index] && session.talks[index].description ? 
                                    `<div class="speaker-talk-desc" style="margin-top: 8px; font-size: 0.85rem; color: #666; font-style: italic;">${session.talks[index].description}</div>` : 
                                    ''
                                }
                            </div>
                        </div>
                    `;
                }).join('')}
            </div>
        `;

        speakersContainer.innerHTML = speakersHTML;
    }

    getParticipantLabel(participantLabel, count) {
        const labels = {
            'speaker': count > 1 ? 'Intervenant·e·s' : 'Intervenant·e',
            'speakers': 'Intervenant·e·s', 
            'participants': 'Participant·e·s',
            'instructors': 'Formateur·rice·s',
            'experts': 'Expert·e·s',
            'panelists': 'Panélistes'
        };
        return labels[participantLabel] || 'Intervenant·e·s';
    }

    getSpeakerTitle(participantLabel) {
        const titles = {
            'speaker': 'Intervenant·e',
            'speakers': 'Intervenant·e',
            'participants': 'Participant·e',
            'instructors': 'Formateur·rice',
            'experts': 'Expert·e Python',
            'panelists': 'Panéliste'
        };
        return titles[participantLabel] || 'Expert·e Python';
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