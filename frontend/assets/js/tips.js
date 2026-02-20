document.addEventListener('DOMContentLoaded', () => {
    fetchTips();
    fetchForecast();
    highlightActivePlan();
});

async function fetchTips() {
    try {
        const data = await apiFetch('/tips/');
        document.getElementById('daily-tip-text').textContent = `"${data.daily_tip}"`;
    } catch (err) {
        console.error('Failed to fetch tips:', err);
    }
}

async function highlightActivePlan() {
    try {
        const data = await apiFetch('/goals/active');

        // 1. Reset ALL cards to default green state first
        [30, 60, 90].forEach(days => {
            const card = document.getElementById(`plan-card-${days}`);
            if (card) {
                card.classList.remove('border-slate-200', 'opacity-80');
                const sidebar = card.querySelector('.w-24'); // sidebar container
                if (sidebar) {
                    sidebar.className = 'w-24 bg-primary/10 flex flex-col items-center justify-center p-2 text-primary group-hover:bg-primary group-hover:text-white transition-colors';
                }
                const btn = card.querySelector('button');
                if (btn) {
                    btn.textContent = 'Select Plan';
                    btn.className = 'bg-primary text-white text-xs px-4 py-1.5 rounded-full font-medium hover:bg-primary/90 transition-colors';
                    btn.classList.remove('cursor-default', 'pointer-events-none');
                }
            }
        });

        // 2. Apply "greyish" neutral styling ONLY to the active plan card
        if (data.has_goal) {
            const planId = `plan-card-${data.target_days}`;
            const card = document.getElementById(planId);
            if (card) {
                const sidebar = card.querySelector('.w-24');
                if (sidebar) {
                    sidebar.className = 'w-24 bg-slate-100 flex flex-col items-center justify-center p-2 text-slate-400 transition-colors';
                }
                const btn = card.querySelector('button');
                if (btn) {
                    btn.textContent = 'Current Plan';
                    btn.className = 'bg-slate-200 text-slate-500 text-xs px-4 py-1.5 rounded-full font-medium cursor-default pointer-events-none';
                }
                card.classList.add('border-slate-200', 'opacity-80');
            }
        }
    } catch (err) {
        console.error('Failed to highlight active plan:', err);
    }
}

async function fetchForecast() {
    try {
        // We can reuse insights or progress for forecast data
        const insights = await apiFetch('/insights/');
        const progress = await apiFetch('/progress/');

        const avg = insights.avg_pages_7_days;
        const pagesLeft = progress.pages_left;
        const isCompleted = progress.is_cycle_completed;

        const daysText = document.getElementById('forecast-days-text');
        const paceText = document.getElementById('forecast-pace-text');
        const bar = document.getElementById('forecast-bar');
        const cardTitle = daysText.previousElementSibling; // "Current Forecast" label

        if (isCompleted) {
            // ── CELEBRATORY STATE ────────────────
            cardTitle.textContent = "الحمد لله";
            cardTitle.classList.add('text-emerald-600', 'font-black', 'mb-1', 'font-diwani', 'text-[2.1rem]', 'leading-tight');
            daysText.textContent = "Congratulations! 🎉";
            daysText.classList.remove('text-2xl');
            daysText.classList.add('text-xl', 'text-emerald-600');

            document.getElementById('forecast-description').innerHTML = `Mabrook! You have completed the Qur'an.`;

            bar.style.width = '100%';
            bar.classList.remove('bg-primary');
            bar.classList.add('bg-emerald-500');
        } else if (avg > 0) {
            // ── NORMAL FORECAST ──────────────────
            cardTitle.textContent = "Current Forecast";
            cardTitle.classList.remove('text-emerald-600', 'font-black', 'mb-2');
            daysText.classList.remove('text-emerald-600');

            const daysToFinish = Math.ceil(pagesLeft / avg);
            daysText.textContent = `${daysToFinish} Days to finish`;

            document.getElementById('forecast-description').innerHTML =
                `Based on your current pace of <span id="forecast-pace-text" class="font-semibold text-primary">${avg} pages per day</span>, you are on track to complete the Qur'an.`;

            bar.style.width = `${progress.progress_percentage}%`;
            bar.classList.add('bg-primary');
            bar.classList.remove('bg-emerald-500');
        } else {
            // ── EMPTY STATE ──────────────────────
            cardTitle.textContent = "Current Forecast";
            cardTitle.classList.remove('text-emerald-600', 'font-black', 'mb-2');
            daysText.textContent = "Start Reading";

            document.getElementById('forecast-description').innerHTML =
                "Log your first reading to see personalized pace and completion estimates.";

            bar.style.width = '0%';
        }
    } catch (err) {
        console.error('Failed to fetch forecast:', err);
    }
}

async function selectPlan(days, pages) {
    try {
        await apiFetch('/goals/', {
            method: 'POST',
            body: JSON.stringify({ target_pages: pages, target_days: days })
        });
        showPlanToast(`${days}-day goal set! 🎉`);
        highlightActivePlan();
    } catch (err) {
        showPlanToast('Could not set goal: ' + err.message, true);
    }
}

function showPlanToast(message, isError = false) {
    const toast = document.getElementById('plan-toast');
    if (!toast) return;
    toast.textContent = message;
    toast.className = `fixed bottom-28 left-1/2 -translate-x-1/2 px-5 py-3 rounded-full text-sm font-semibold shadow-lg transition-all duration-300 ${isError ? 'bg-red-500 text-white' : 'bg-emerald-600 text-white'}`;
    toast.classList.remove('opacity-0', 'pointer-events-none');
    setTimeout(() => {
        toast.classList.add('opacity-0', 'pointer-events-none');
    }, 2500);
}
