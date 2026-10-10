/**
 * CodeQuiz - Client-side Quiz Engine
 * Handles countdown timer, question navigation, option selection,
 * keyboard shortcuts, web audio feedback, and automatic submission.
 */

class QuizEngine {
    constructor(config) {
        this.questions = config.questions || [];
        this.topicSlug = config.topicSlug;
        this.difficulty = config.difficulty;
        this.timerMode = config.timerMode || 'per_question'; // 'per_question', 'total', 'practice'
        this.totalTimeLimit = config.totalTimeLimit || 300;
        this.submitUrl = config.submitUrl;

        this.currentIndex = 0;
        this.userAnswers = {}; // { question_id: { selected: 'A', time: 10 } }
        this.flaggedQuestions = new Set();
        this.questionStartTimestamp = Date.now();
        this.totalTimeSpentSeconds = 0;
        this.timerInterval = null;
        this.soundMuted = false;

        // Per-question timer config
        this.secondsRemaining = this.getInitialTime();

        // Audio Context (Web Audio API synth)
        this.initAudio();

        // Bind DOM Elements
        this.dom = {
            timerDisplay: document.getElementById('timer-display'),
            timerBadge: document.getElementById('timer-badge'),
            qCounter: document.getElementById('q-counter'),
            qDifficulty: document.getElementById('q-difficulty'),
            qText: document.getElementById('q-text'),
            codeSnippetWrapper: document.getElementById('code-snippet-wrapper'),
            codeElement: document.getElementById('code-element'),
            optionsContainer: document.getElementById('options-container'),
            progressBar: document.getElementById('quiz-progress-bar'),
            navDrawer: document.getElementById('nav-drawer'),
            prevBtn: document.getElementById('prev-btn'),
            nextBtn: document.getElementById('next-btn'),
            flagBtn: document.getElementById('flag-btn'),
            muteBtn: document.getElementById('mute-btn'),
            submitModalBtn: document.getElementById('submit-modal-btn'),
            submissionForm: document.getElementById('quiz-submission-form'),
            payloadInput: document.getElementById('quiz-payload-input')
        };

        this.init();
    }

    initAudio() {
        try {
            const AudioContext = window.AudioContext || window.webkitAudioContext;
            this.audioCtx = AudioContext ? new AudioContext() : null;
        } catch (e) {
            this.audioCtx = null;
        }
    }

    playTone(frequency, type = 'sine', duration = 0.1) {
        if (this.soundMuted || !this.audioCtx) return;
        try {
            if (this.audioCtx.state === 'suspended') {
                this.audioCtx.resume();
            }
            const osc = this.audioCtx.createOscillator();
            const gain = this.audioCtx.createGain();
            osc.type = type;
            osc.frequency.setValueAtTime(frequency, this.audioCtx.currentTime);
            gain.gain.setValueAtTime(0.08, this.audioCtx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.001, this.audioCtx.currentTime + duration);
            osc.connect(gain);
            gain.connect(this.audioCtx.destination);
            osc.start();
            osc.stop(this.audioCtx.currentTime + duration);
        } catch (e) {}
    }

    getInitialTime() {
        if (this.timerMode === 'practice') return 99999;
        if (this.timerMode === 'total') return this.totalTimeLimit;
        const currentQ = this.questions[this.currentIndex];
        return currentQ ? currentQ.time_limit_sec : 30;
    }

    init() {
        if (!this.questions.length) return;

        this.renderDrawer();
        this.renderQuestion(0);
        this.setupEventListeners();
        this.startTimer();
    }

    setupEventListeners() {
        if (this.dom.prevBtn) {
            this.dom.prevBtn.addEventListener('click', () => this.prevQuestion());
        }
        if (this.dom.nextBtn) {
            this.dom.nextBtn.addEventListener('click', () => {
                if (this.currentIndex === this.questions.length - 1) {
                    this.confirmSubmit();
                } else {
                    this.nextQuestion();
                }
            });
        }
        if (this.dom.flagBtn) {
            this.dom.flagBtn.addEventListener('click', () => this.toggleFlag());
        }
        if (this.dom.muteBtn) {
            this.dom.muteBtn.addEventListener('click', () => {
                this.soundMuted = !this.soundMuted;
                this.dom.muteBtn.innerHTML = this.soundMuted
                    ? '<i class="fa-solid fa-volume-xmark text-secondary"></i>'
                    : '<i class="fa-solid fa-volume-high text-info"></i>';
            });
        }
        if (this.dom.submitModalBtn) {
            this.dom.submitModalBtn.addEventListener('click', () => this.submitQuiz());
        }

        // Keyboard Shortcuts (A/B/C/D or 1/2/3/4, Arrows for nav)
        document.addEventListener('keydown', (e) => {
            // Ignore if active input
            if (['input', 'textarea'].includes(document.activeElement.tagName.toLowerCase())) return;

            const key = e.key.toUpperCase();
            if (['A', '1'].includes(key)) this.selectOption('A');
            else if (['B', '2'].includes(key)) this.selectOption('B');
            else if (['C', '3'].includes(key)) this.selectOption('C');
            else if (['D', '4'].includes(key)) this.selectOption('D');
            else if (key === 'ARROWLEFT' && this.currentIndex > 0) this.prevQuestion();
            else if (key === 'ARROWRIGHT') {
                if (this.currentIndex < this.questions.length - 1) this.nextQuestion();
            }
            else if (key === 'F') this.toggleFlag();
        });
    }

    renderDrawer() {
        if (!this.dom.navDrawer) return;
        this.dom.navDrawer.innerHTML = '';
        this.questions.forEach((q, idx) => {
            const pill = document.createElement('div');
            pill.className = 'q-pill';
            pill.id = `q-pill-${idx}`;
            pill.textContent = idx + 1;
            pill.title = `Question ${idx + 1}`;
            pill.addEventListener('click', () => {
                this.recordQuestionTime();
                this.renderQuestion(idx);
            });
            this.dom.navDrawer.appendChild(pill);
        });
    }

    updateDrawerState() {
        this.questions.forEach((q, idx) => {
            const pill = document.getElementById(`q-pill-${idx}`);
            if (!pill) return;

            pill.classList.remove('active', 'answered', 'flagged');
            if (idx === this.currentIndex) {
                pill.classList.add('active');
            } else if (this.userAnswers[q.id]?.selected) {
                pill.classList.add('answered');
            }

            if (this.flaggedQuestions.has(q.id)) {
                pill.classList.add('flagged');
            }
        });
    }

    renderQuestion(index) {
        this.currentIndex = index;
        const q = this.questions[index];
        if (!q) return;

        // Reset question start time
        this.questionStartTimestamp = Date.now();

        // If per_question timer, reset countdown for this question
        if (this.timerMode === 'per_question') {
            this.secondsRemaining = q.time_limit_sec || 30;
            this.updateTimerDisplay();
        }

        // Counter & Header
        if (this.dom.qCounter) {
            this.dom.qCounter.textContent = `Question ${index + 1} of ${this.questions.length}`;
        }
        if (this.dom.qDifficulty) {
            this.dom.qDifficulty.textContent = q.difficulty;
            this.dom.qDifficulty.className = `badge font-monospace ${
                q.difficulty === 'Beginner' ? 'bg-success-subtle text-success border border-success-subtle' :
                q.difficulty === 'Intermediate' ? 'bg-warning-subtle text-warning border border-warning-subtle' :
                'bg-danger-subtle text-danger border border-danger-subtle'
            }`;
        }

        // Question Text
        if (this.dom.qText) {
            this.dom.qText.textContent = q.question_text;
        }

        // Code Snippet with Syntax Highlighting
        if (this.dom.codeSnippetWrapper && this.dom.codeElement) {
            if (q.code_snippet && q.code_snippet.trim() !== '') {
                this.dom.codeSnippetWrapper.style.display = 'block';
                this.dom.codeElement.className = `language-${q.code_lang || 'javascript'}`;
                this.dom.codeElement.textContent = q.code_snippet;
                if (window.Prism) {
                    Prism.highlightElement(this.dom.codeElement);
                }
            } else {
                this.dom.codeSnippetWrapper.style.display = 'none';
            }
        }

        // Options A, B, C, D
        if (this.dom.optionsContainer) {
            this.dom.optionsContainer.innerHTML = '';
            const options = [
                { letter: 'A', text: q.option_a },
                { letter: 'B', text: q.option_b },
                { letter: 'C', text: q.option_c },
                { letter: 'D', text: q.option_d }
            ];

            const currentSelected = this.userAnswers[q.id]?.selected;

            options.forEach(opt => {
                const card = document.createElement('div');
                card.className = `option-card ${currentSelected === opt.letter ? 'selected' : ''}`;
                card.setAttribute('data-option', opt.letter);
                card.innerHTML = `
                    <div class="option-letter-badge">${opt.letter}</div>
                    <div class="option-text">${this.escapeHtml(opt.text)}</div>
                    <span class="badge bg-dark-subtle text-muted font-monospace d-none d-md-inline-block small">Press ${opt.letter}</span>
                `;
                card.addEventListener('click', () => this.selectOption(opt.letter));
                this.dom.optionsContainer.appendChild(card);
            });
        }

        // Flag button state
        if (this.dom.flagBtn) {
            const isFlagged = this.flaggedQuestions.has(q.id);
            this.dom.flagBtn.innerHTML = isFlagged
                ? '<i class="fa-solid fa-flag text-warning"></i> Flagged'
                : '<i class="fa-regular fa-flag"></i> Flag';
        }

        // Buttons
        if (this.dom.prevBtn) {
            this.dom.prevBtn.disabled = index === 0;
        }
        if (this.dom.nextBtn) {
            if (index === this.questions.length - 1) {
                this.dom.nextBtn.innerHTML = 'Submit Quiz <i class="fa-solid fa-check ms-1"></i>';
                this.dom.nextBtn.className = 'btn btn-success px-4 fw-semibold rounded-pill';
            } else {
                this.dom.nextBtn.innerHTML = 'Next <i class="fa-solid fa-arrow-right ms-1"></i>';
                this.dom.nextBtn.className = 'btn btn-primary px-4 fw-semibold rounded-pill';
            }
        }

        // Progress Bar
        if (this.dom.progressBar) {
            const pct = Math.round(((index + 1) / this.questions.length) * 100);
            this.dom.progressBar.style.width = `${pct}%`;
        }

        this.updateDrawerState();
    }

    recordQuestionTime() {
        const q = this.questions[this.currentIndex];
        if (!q) return;

        const timeSpent = Math.max(1, Math.round((Date.now() - this.questionStartTimestamp) / 1000));
        this.totalTimeSpentSeconds += timeSpent;

        if (!this.userAnswers[q.id]) {
            this.userAnswers[q.id] = { selected: null, time: timeSpent };
        } else {
            this.userAnswers[q.id].time = (this.userAnswers[q.id].time || 0) + timeSpent;
        }
    }

    selectOption(letter) {
        const q = this.questions[this.currentIndex];
        if (!q) return;

        this.recordQuestionTime();
        this.userAnswers[q.id].selected = letter;

        // Play feedback sound
        this.playTone(520, 'sine', 0.12);

        // Update UI
        const optionCards = this.dom.optionsContainer.querySelectorAll('.option-card');
        optionCards.forEach(card => {
            if (card.getAttribute('data-option') === letter) {
                card.classList.add('selected');
            } else {
                card.classList.remove('selected');
            }
        });

        this.updateDrawerState();
    }

    toggleFlag() {
        const q = this.questions[this.currentIndex];
        if (!q) return;

        if (this.flaggedQuestions.has(q.id)) {
            this.flaggedQuestions.delete(q.id);
        } else {
            this.flaggedQuestions.add(q.id);
            this.playTone(400, 'triangle', 0.1);
        }

        this.renderQuestion(this.currentIndex);
    }

    nextQuestion() {
        this.recordQuestionTime();
        if (this.currentIndex < this.questions.length - 1) {
            this.renderQuestion(this.currentIndex + 1);
        }
    }

    prevQuestion() {
        this.recordQuestionTime();
        if (this.currentIndex > 0) {
            this.renderQuestion(this.currentIndex - 1);
        }
    }

    startTimer() {
        if (this.timerMode === 'practice') {
            if (this.dom.timerDisplay) this.dom.timerDisplay.textContent = 'Practice';
            return;
        }

        this.updateTimerDisplay();

        this.timerInterval = setInterval(() => {
            this.secondsRemaining--;
            this.updateTimerDisplay();

            // Sound tick when timer is critical (< 5s)
            if (this.secondsRemaining <= 5 && this.secondsRemaining > 0) {
                this.playTone(800, 'square', 0.05);
            }

            if (this.secondsRemaining <= 0) {
                this.handleTimeExpiry();
            }
        }, 1000);
    }

    handleTimeExpiry() {
        this.recordQuestionTime();
        this.playTone(220, 'sawtooth', 0.3);

        if (this.timerMode === 'per_question') {
            // If more questions exist, auto-advance
            if (this.currentIndex < this.questions.length - 1) {
                this.nextQuestion();
            } else {
                // Last question expired - auto-submit!
                clearInterval(this.timerInterval);
                this.submitQuiz();
            }
        } else {
            // Total quiz timer expired - auto-submit!
            clearInterval(this.timerInterval);
            this.submitQuiz();
        }
    }

    updateTimerDisplay() {
        if (!this.dom.timerDisplay) return;

        const minutes = Math.floor(Math.max(0, this.secondsRemaining) / 60);
        const seconds = Math.max(0, this.secondsRemaining) % 60;
        const formatted = `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
        this.dom.timerDisplay.textContent = formatted;

        // Visual urgency states
        if (this.dom.timerBadge) {
            this.dom.timerBadge.classList.remove('timer-warning', 'timer-danger');
            if (this.secondsRemaining <= 5) {
                this.dom.timerBadge.classList.add('timer-danger');
            } else if (this.secondsRemaining <= 10) {
                this.dom.timerBadge.classList.add('timer-warning');
            }
        }
    }

    confirmSubmit() {
        const answeredCount = Object.values(this.userAnswers).filter(a => a.selected).length;
        const unansweredCount = this.questions.length - answeredCount;

        // Populate modal summary text
        const summaryText = document.getElementById('submit-modal-summary');
        if (summaryText) {
            summaryText.innerHTML = `
                You have answered <strong>${answeredCount}</strong> of <strong>${this.questions.length}</strong> questions.<br>
                ${unansweredCount > 0 ? `<span class="text-warning"><i class="fa-solid fa-triangle-exclamation me-1"></i>${unansweredCount} questions remain unanswered and will be marked as skipped.</span>` : '<span class="text-success"><i class="fa-solid fa-circle-check me-1"></i>All questions answered! Great job!</span>'}
            `;
        }

        const modalEl = document.getElementById('submitConfirmModal');
        if (modalEl && window.bootstrap) {
            const modal = new bootstrap.Modal(modalEl);
            modal.show();
        } else {
            if (confirm(`Submit quiz? You answered ${answeredCount}/${this.questions.length} questions.`)) {
                this.submitQuiz();
            }
        }
    }

    submitQuiz() {
        this.recordQuestionTime();
        if (this.timerInterval) clearInterval(this.timerInterval);

        // Fill unanswered questions with null
        this.questions.forEach(q => {
            if (!this.userAnswers[q.id]) {
                this.userAnswers[q.id] = { selected: null, time: 0 };
            }
        });

        const payload = {
            topic_slug: this.topicSlug,
            difficulty: this.difficulty,
            total_time_spent: this.totalTimeSpentSeconds,
            answers: this.userAnswers
        };

        if (this.dom.submissionForm && this.dom.payloadInput) {
            this.dom.payloadInput.value = JSON.stringify(payload);
            this.dom.submissionForm.submit();
        } else {
            // Fallback AJAX submit
            fetch(this.submitUrl, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            })
            .then(res => res.json())
            .then(data => {
                if (data.redirect_url) {
                    window.location.href = data.redirect_url;
                }
            })
            .catch(err => {
                console.error('Submission failed', err);
                alert('Submission error. Please retry.');
            });
        }
    }

    escapeHtml(text) {
        if (!text) return '';
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

window.QuizEngine = QuizEngine;
