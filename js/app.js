function playConsultationVideo() {
    const stages = document.querySelectorAll('.consultation-stage');
    let currentStage = 0;

    function showStage(stageIndex) {
        stages.forEach(s => s.classList.remove('active'));
        if (stages[stageIndex]) {
            stages[stageIndex].classList.add('active');
        }
    }

    function nextStage() {
        showStage(currentStage);

        if (currentStage === 0) {
            setTimeout(() => { currentStage = 1; nextStage(); }, 1500);
        } else if (currentStage === 1) {
            setTimeout(() => { currentStage = 2; nextStage(); }, 2500);
        } else if (currentStage === 2) {
            setTimeout(() => { currentStage = 3; nextStage(); }, 3000);
        } else if (currentStage === 3) {
            setTimeout(() => { currentStage = 0; nextStage(); }, 3500);
        }
    }

    nextStage();
}

// Initialize on Load
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}

function init() {
    playConsultationVideo();
    setupScrollAnimations();
}

function setupScrollAnimations() {
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.15 // Trigger when 15% visible
    };

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('in-view');
                // Optional: Stop observing once triggered if you want it to run only once
                // observer.unobserve(entry.target); 
            } else {
                // Optional: Remove class to replay animation when scrolling back up
                entry.target.classList.remove('in-view');
            }
        });
    }, observerOptions);

    const animatedElements = document.querySelectorAll('.animate-when-visible, .fade-up');
    animatedElements.forEach(el => observer.observe(el));
}
