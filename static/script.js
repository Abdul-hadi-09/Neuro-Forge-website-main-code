document.addEventListener('DOMContentLoaded', () => {
    // Mobile Menu Toggle
    const mobileMenu = document.getElementById('mobile-menu');
    const navMenu = document.querySelector('.nav-menu');

    if (mobileMenu) {
        mobileMenu.addEventListener('click', () => {
            mobileMenu.classList.toggle('active');
            navMenu.classList.toggle('active');
        });
    }

    // Close mobile menu when clicking a link
    document.querySelectorAll('.nav-link').forEach(n => n.addEventListener('click', () => {
        mobileMenu.classList.remove('active');
        navMenu.classList.remove('active');
    }));

    // Mouse move effect for service cards
    const cards = document.querySelectorAll('.service-card');
    document.addEventListener('mousemove', (e) => {
        cards.forEach(card => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;

            card.style.setProperty('--mouse-x', `${x}px`);
            card.style.setProperty('--mouse-y', `${y}px`);
        });
    });

    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
});

// Scroll Animation Observer
const observerOptions = {
    root: null,
    rootMargin: '0px',
    threshold: 0.05
};

const observer = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('show-section');
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);

const sections = document.querySelectorAll('section, header, .footer');
sections.forEach(section => {
    section.classList.add('hidden-section');
    observer.observe(section);
});

// Individual Card Scroll Animation (Staggered)
const cardObserverOptions = {
    threshold: 0.05, // Trigger when 15% of the card is visible
    rootMargin: '0px 0px -20px 0px'
};

const cardObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach((entry, index) => {
        if (entry.isIntersecting) {
            // Add delay based on index in the current batch of intersecting entries
            // This ensures if 3 cards appear at once, they stagger.
            // If scanning one by one on mobile, index is 0, so no delay (instant).
            setTimeout(() => {
                entry.target.classList.add('show-card');
            }, index * 100);

            observer.unobserve(entry.target);
        }
    });
}, cardObserverOptions);

// Select all individual items/cards to animate
const animatedCards = document.querySelectorAll('.service-card, .feature-item, .testimonial-card, .stat-item, .process-step, .portfolio-card');
animatedCards.forEach(card => {
    card.classList.add('hidden-card');
    cardObserver.observe(card);
});


// Quote Wizard Logic
document.addEventListener('DOMContentLoaded', () => {
    const wizardForm = document.getElementById('quote-form');
    if (!wizardForm) return;

    const steps = document.querySelectorAll('.form-step');
    const indicatorSteps = document.querySelectorAll('.progress-step');
    const nextBtns = document.querySelectorAll('.next-step');
    const prevBtns = document.querySelectorAll('.prev-step');
    let currentStep = 1;

    // Next Button Click
    nextBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const nextStepNum = parseInt(btn.dataset.next);
            if (validateStep(currentStep)) {
                goToStep(nextStepNum);
            }
        });
    });

    // Previous Button Click
    prevBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const prevStepNum = parseInt(btn.dataset.prev);
            goToStep(prevStepNum);
        });
    });

    function goToStep(stepNum) {
        // Hide all steps
        steps.forEach(step => step.classList.remove('active'));
        // Show target step
        document.getElementById('step-' + stepNum).classList.add('active');

        // Update indicators
        indicatorSteps.forEach(indicator => {
            const indicatorNum = parseInt(indicator.dataset.step);
            indicator.classList.remove('active', 'completed');
            if (indicatorNum === stepNum) {
                indicator.classList.add('active');
            } else if (indicatorNum < stepNum) {
                indicator.classList.add('completed');
            }
        });

        currentStep = stepNum;

        // Scroll to top of wizard
        document.querySelector('.quote-wizard-container').scrollIntoView({ behavior: 'smooth' });
    }

    function validateStep(stepNum) {
        const stepEl = document.getElementById('step-' + stepNum);
        const requiredInputs = stepEl.querySelectorAll('input[required], select[required], textarea[required]');
        let isValid = true;
        let firstError = null;

        requiredInputs.forEach(input => {
            if (!input.value.trim()) {
                isValid = false;
                input.style.borderColor = '#ef4444';
                if (!firstError) firstError = input;

                // Add shake animation or error msg listener
                input.addEventListener('input', () => {
                    input.style.borderColor = '';
                }, { once: true });
            }
        });

        if (!isValid && firstError) {
            firstError.focus();
            // Optional: Shake effect
        }

        return isValid;
    }
});

