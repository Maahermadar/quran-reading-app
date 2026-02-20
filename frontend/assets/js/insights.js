document.addEventListener('DOMContentLoaded', () => {
    fetchInsights();
});

async function fetchInsights() {
    try {
        const data = await apiFetch('/insights/');
        updateUI(data);
    } catch (err) {
        console.error('Failed to fetch insights:', err);
    }
}

function updateUI(data) {
    document.getElementById('avg-pages-text').textContent = data.avg_pages_7_days;
    document.getElementById('current-streak-text').textContent = data.streak;
    document.getElementById('est-days-text').textContent = data.est_days_for_100_pages;
    document.getElementById('best-time-text').textContent = data.best_time;
    document.getElementById('weekly-total-text').textContent = data.weekly_total;

    // Render Weekly Chart
    const chartContainer = document.getElementById('weekly-chart-container');
    if (chartContainer && data.daily_stats) {
        chartContainer.innerHTML = '';
        data.daily_stats.forEach(stat => {
            const bar = document.createElement('div');
            // Different styling for today vs other days or active vs inactive
            const bgClass = stat.is_today ? 'bg-primary/20 border border-primary/20' : (stat.pages > 0 ? 'bg-primary/10' : 'bg-slate-50 dark:bg-slate-800/50');
            const textClass = stat.pages > 0 ? 'text-slate-700 dark:text-slate-200' : 'text-slate-400';

            bar.className = `flex flex-col items-center py-3 ${bgClass} rounded-lg`;
            bar.innerHTML = `
                <span class="text-[10px] font-medium text-slate-400 uppercase mb-1">${stat.day}</span>
                <span class="text-sm font-bold ${textClass}">${stat.pages}</span>
            `;
            chartContainer.appendChild(bar);
        });
    }

    if (data.total_logs > 0) {
        document.getElementById('personal-insight-text').innerHTML = `
            You have recorded <span class="font-bold text-primary">${data.total_logs} sessions</span> in total. 
            Your longest reading streak is <span class="font-bold text-primary">${data.longest_streak} days</span>.
            At your current pace, you'll finish the next 100 pages in <span class="font-bold text-primary">${data.est_days_for_100_pages} days</span>.
        `;
    }
}
