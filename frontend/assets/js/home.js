document.addEventListener('DOMContentLoaded', () => {
    // Show UI immediately. Skeletons are visible by default in HTML.
    // Individual update functions will check for cache during their execution.

    // Trigger parallel fetches without awaiting them to unblock UI
    fetchProgress();
    fetchGoals();
    fetchStreak();

    // Attach form handlers
    const readingForm = document.getElementById('reading-form');
    if (readingForm) {
        readingForm.addEventListener('submit', handleReadingSubmit);
    }

    const goalForm = document.getElementById('goal-form');
    if (goalForm) {
        goalForm.addEventListener('submit', handleGoalSubmit);
    }
});

async function fetchProgress() {
    try {
        const data = await apiFetch('/progress/');
        updateProgressUI(data);
    } catch (err) {
        console.error('Failed to fetch progress:', err);
    }
}

async function fetchGoals() {
    try {
        const data = await apiFetch('/goals/active');
        const container = document.getElementById('active-goal-container');
        const noGoal = document.getElementById('no-goal-container');

        if (data.has_goal && data.pages_left === 0) {
            // ── COMPLETED STATE ────────────────
            container.classList.remove('hidden');
            noGoal.classList.add('hidden');
            container.innerHTML = `
                <div class="relative overflow-hidden">
                    <div class="flex justify-between items-center mb-8">
                        <div class="flex items-center gap-2">
                            <span class="material-symbols-outlined text-emerald-600/60 text-lg">flag</span>
                            <p class="text-sm font-bold text-slate-700 dark:text-slate-200">${data.target_pages} Pages in ${data.target_days} Days</p>
                        </div>
                        <span class="text-[9px] font-black text-emerald-600 bg-emerald-100 dark:bg-emerald-900/40 px-2 py-1 rounded-md uppercase tracking-tighter">Achieved</span>
                    </div>

                    <div class="flex flex-col gap-1 pb-8">
                        <h3 class="text-xl font-bold text-slate-900 dark:text-white flex items-center gap-2">
                            Goal Completed 
                            <span class="material-symbols-outlined text-emerald-500 font-bold">check_circle</span>
                        </h3>
                        <p class="text-sm text-slate-500 dark:text-slate-400">You've finished your goal — amazing work!</p>
                    </div>

                    <button onclick="openGoalModal()"
                        class="w-full bg-emerald-100/60 dark:bg-emerald-900/40 text-emerald-700 dark:text-emerald-300 py-3 rounded-xl font-semibold transition-all flex items-center justify-center gap-2 hover:bg-emerald-200/60 dark:hover:bg-emerald-900/60">
                        <span class="material-symbols-outlined text-lg">add_circle</span>
                        Set New Goal
                    </button>
                </div>
            `;

        } else if (data.has_goal) {
            // ── IN-PROGRESS STATE ────────────────────────────────────────
            container.classList.remove('hidden');
            noGoal.classList.add('hidden');
            container.innerHTML = `
                <div class="flex justify-between items-center gap-4 flex-nowrap">
                    <div class="flex items-center gap-2 min-w-0">
                        <span class="material-symbols-outlined text-primary text-xl shrink-0">flag</span>
                        <p class="font-bold text-slate-800 dark:text-slate-100 truncate">${data.target_pages} Pages in ${data.target_days} Days</p>
                    </div>
                    <span class="text-xs font-bold text-primary bg-primary/10 px-3 py-1 rounded-full uppercase tracking-tight shrink-0 whitespace-nowrap">${data.progress_percentage}% DONE</span>
                </div>
                <div class="grid grid-cols-2 gap-4">
                    <div class="bg-accent-soft/30 dark:bg-primary/5 p-4 rounded-xl border border-primary/5 text-center">
                        <p class="text-[10px] text-slate-500 uppercase font-bold tracking-widest mb-1">Remaining</p>
                        <p class="text-4xl font-extrabold text-primary dark:text-slate-100">${data.pages_left}</p>
                        <p class="text-xs font-medium text-slate-400">Pages</p>
                    </div>
                    <div class="bg-accent-soft/30 dark:bg-primary/5 p-4 rounded-xl border border-primary/5 text-center">
                        <p class="text-[10px] text-slate-500 uppercase font-bold tracking-widest mb-1">Days Left</p>
                        <p class="text-4xl font-extrabold text-slate-700 dark:text-slate-200">${data.days_left}</p>
                        <p class="text-xs font-medium text-slate-400">${data.days_left === 1 ? 'Day' : 'Days'}</p>
                    </div>
                </div>
                <div class="space-y-2 pt-2">
                    <div class="w-full h-3 bg-accent-soft dark:bg-slate-800 rounded-full overflow-hidden">
                        <div class="h-full bg-primary rounded-full transition-all duration-1000" style="width: ${data.progress_percentage}%;"></div>
                    </div>
                </div>
            `;

        } else {
            // ── NO GOAL STATE ────────────────────────────────
            container.classList.add('hidden');
            noGoal.classList.remove('hidden');
        }
    } catch (err) {
        console.error('Failed to fetch goals:', err);
    }
}

async function fetchStreak() {
    try {
        const data = await apiFetch('/insights/');
        const streakEl = document.getElementById('streak-text');
        streakEl.textContent = `${data.streak} Day Streak`;
        streakEl.classList.remove('skeleton-text', 'skeleton', 'w-24');
    } catch (err) {
        console.error('Failed to fetch streak:', err);
    }
}

function updateProgressUI(data) {
    const juzText = document.getElementById('current-juz-text');
    const surahEnText = document.getElementById('surah-name-en-text');
    const surahArText = document.getElementById('surah-name-ar-text');
    const progressBadge = document.getElementById('progress-percentage-badge');
    const pagesReadText = document.getElementById('pages-read-text');
    const pagesLeftText = document.getElementById('pages-left-text');
    const lifetimeCount = document.getElementById('lifetime-completions-count');

    if (juzText) {
        juzText.textContent = `Juz ${data.juz}`;
        juzText.classList.remove('skeleton-text', 'skeleton', 'w-24');
    }

    if (surahEnText) {
        surahEnText.textContent = data.surah_name_en;
        surahEnText.classList.remove('skeleton-text', 'skeleton', 'w-32');
    }

    if (surahArText) {
        surahArText.textContent = data.surah_name_ar;
        surahArText.classList.remove('skeleton-text', 'skeleton', 'w-24');
    }

    if (progressBadge) {
        progressBadge.textContent = `${data.progress_percentage}% Done`;
        progressBadge.classList.remove('skeleton-text', 'skeleton');
    }

    if (pagesReadText) {
        pagesReadText.textContent = `Page ${data.current_page} of 604`;
        pagesReadText.classList.remove('skeleton-text', 'skeleton', 'w-24');
    }

    if (pagesLeftText) {
        pagesLeftText.textContent = `${data.pages_left} pages left`;
        pagesLeftText.classList.remove('skeleton-text', 'skeleton', 'w-24');
    }

    const fill = document.getElementById('progress-bar-fill');
    if (fill) fill.style.width = `${data.progress_percentage}%`;

    if (lifetimeCount) {
        lifetimeCount.textContent = data.lifetime_completions;
        lifetimeCount.classList.remove('skeleton-text', 'skeleton', 'w-12');
    }

    // Show/hide Quran completion banner based on backend state
    const completionMsg = document.getElementById('completion-success-message');
    if (completionMsg) {
        if (data.is_cycle_completed) {
            completionMsg.classList.remove('hidden');
        } else {
            completionMsg.classList.add('hidden');
        }
    }
}

function openModal() {
    const modal = document.getElementById('recording-modal');
    modal.classList.remove('hidden');

    const startInput = document.getElementById('start-page');
    const endInput = document.getElementById('end-page');
    const errorMsg = document.getElementById('page-error-msg');
    const submitBtn = document.querySelector('#reading-form button[type="submit"]');

    // Initial state
    startInput.value = '';
    endInput.value = '';
    endInput.classList.remove('border-red-500');
    if (errorMsg) errorMsg.classList.add('hidden');
    submitBtn.disabled = true;

    // Fetch progress to determine Effective Last Page
    apiFetch('/progress/').then(progress => {
        // If cycle completed, effective last page is 1
        const effectiveLastPage = progress.is_cycle_completed ? 1 : progress.current_page;

        startInput.value = effectiveLastPage;
        endInput.min = effectiveLastPage;
        endInput.max = 604;
        endInput.placeholder = `Min ${effectiveLastPage}`;

        // Setup validation listener
        const validate = () => {
            const val = parseInt(endInput.value);
            let errorMessage = "";

            if (!endInput.value) {
                errorMessage = ""; // Button remains disabled (opacity logic below)
            } else if (isNaN(val) || val < effectiveLastPage) {
                errorMessage = `Please enter a page starting from ${effectiveLastPage}`;
            } else if (val > 604) {
                errorMessage = "The maximum page in this Mushaf is 604";
            }

            if (errorMessage) {
                const textSpan = errorMsg.querySelector('.msg-text');
                if (textSpan) textSpan.textContent = errorMessage;
                errorMsg.classList.remove('hidden');
                errorMsg.classList.add('flex');
                endInput.classList.add('border-red-500', 'bg-red-50/50', 'dark:bg-red-900/10');
                submitBtn.disabled = true;
                submitBtn.style.opacity = "0.3";
            } else {
                errorMsg.classList.add('hidden');
                errorMsg.classList.remove('flex');
                endInput.classList.remove('border-red-500', 'bg-red-50/50', 'dark:bg-red-900/10');
                submitBtn.disabled = !endInput.value;
                submitBtn.style.opacity = endInput.value ? "1" : "0.3";
            }
        };

        endInput.oninput = validate;
        endInput.focus();
    }).catch(err => console.error('Failed to pre-fill modal:', err));
}

function closeModal() {
    document.getElementById('recording-modal').classList.add('hidden');
}

function openGoalModal() {
    const modal = document.getElementById('goal-modal');
    if (modal) {
        modal.classList.remove('hidden');
    }
}

function closeGoalModal() {
    document.getElementById('goal-modal').classList.add('hidden');
}

async function handleGoalSubmit(e) {
    e.preventDefault();
    const targetPages = parseInt(document.getElementById('goal-target-pages').value);
    const targetDays = parseInt(document.getElementById('goal-target-days').value);
    const submitBtn = e.target.querySelector('button[type="submit"]');

    submitBtn.disabled = true;
    try {
        await apiFetch('/goals/', {
            method: 'POST',
            body: JSON.stringify({ target_pages: targetPages, target_days: targetDays })
        });
        closeGoalModal();
        fetchGoals();
    } catch (err) {
        alert('Error setting goal: ' + err.message);
    } finally {
        submitBtn.disabled = false;
    }
}

async function handleReadingSubmit(e) {
    e.preventDefault();
    const startPage = parseInt(document.getElementById('start-page').value);
    const endPage = parseInt(document.getElementById('end-page').value);
    const submitBtn = e.target.querySelector('button[type="submit"]');

    // Disable save button while request is in-flight — prevents double submissions
    submitBtn.disabled = true;
    submitBtn.textContent = 'Saving…';

    try {
        await apiFetch('/logs/', {
            method: 'POST',
            body: JSON.stringify({ start_page: startPage, end_page: endPage })
        });
        closeModal();
        // Refresh all summaries after save
        await Promise.all([fetchProgress(), fetchGoals(), fetchStreak()]);
    } catch (err) {
        alert('Error saving reading: ' + err.message);
    } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = 'Save Reading';
    }
}
