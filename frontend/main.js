document.getElementById('btn-analyze').addEventListener('click', analyzeRepo);
document.getElementById('repo-input').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') analyzeRepo();
});

async function analyzeRepo() {
    const input = document.getElementById('repo-input').value.trim();
    const errorEl = document.getElementById('error-msg');
    const dashboard = document.getElementById('dashboard');
    
    if (!input.includes('/')) {
        showError("Please use the format 'owner/repo'");
        return;
    }

    try {
        errorEl.classList.add('hidden');
        const [owner, repo] = input.split('/');
        
        const response = await fetch(`/api/metrics/${owner}/${repo}`);
        const data = await response.json();
        
        if (!response.ok) throw new Error(data.error || 'Failed to fetch data');
        
        renderDashboard(data);
    } catch (error) {
        showError(error.message);
    }
}

function showError(msg) {
    const errorEl = document.getElementById('error-msg');
    const dashboard = document.getElementById('dashboard');
    errorEl.textContent = msg;
    errorEl.classList.remove('hidden');
    dashboard.classList.add('hidden');
}

function renderDashboard(data) {
    document.getElementById('dashboard').classList.remove('hidden');
    document.getElementById('repo-name').textContent = data.name;
    document.getElementById('repo-desc').textContent = data.description;
    
    document.getElementById('stat-stars').textContent = data.stars.toLocaleString();
    document.getElementById('stat-forks').textContent = data.forks.toLocaleString();
    document.getElementById('stat-issues').textContent = data.issues.toLocaleString();

    const maxVal = Math.max(data.stars, data.forks, data.issues, 1);
    document.getElementById('bar-stars').style.width = `${(data.stars / maxVal) * 100}%`;
    document.getElementById('bar-forks').style.width = `${(data.forks / maxVal) * 100}%`;
    document.getElementById('bar-issues').style.width = `${(data.issues / maxVal) * 100}%`;
}