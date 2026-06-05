const dashboardData = {
    admin: {
        title: "Admin Control Center",
        stats: [
            { label: "Nodes", val: "1,245", icon: "fa-server" },
            { label: "Modules", val: "320", icon: "fa-project-diagram" },
            { label: "Experts", val: "85", icon: "fa-user-shield" },
            { label: "Revenue", val: "₹1.25L", icon: "fa-microchip" }
        ],
        activities: ["System Patch 2.4 Applied", "New Tutor Request: AI Ethics", "Backup Completed"]
    },
    student: {
        title: "Student Portal",
        stats: [
            { label: "Courses", val: "4", icon: "fa-graduation-cap" },
            { label: "Knowledge", val: "12", icon: "fa-brain" },
            { label: "Learning", val: "45h", icon: "fa-bolt" },
            { label: "Rank", val: "#5", icon: "fa-medal" }
        ],
        activities: ["Earned: Python Basics Badge", "New Assignment: Data Structures", "Quiz Score: 98%"]
    },
    tutor: {
        title: "Tutor Console",
        stats: [
            { label: "Learners", val: "450", icon: "fa-network-wired" },
            { label: "Rating", val: "4.8", icon: "fa-star" },
            { label: "Completion", val: "78%", icon: "fa-chart-pie" },
            { label: "Earnings", val: "₹45K", icon: "fa-credit-card" }
        ],
        activities: ["12 Pending Assignments", "Live Stream Scheduled: 4 PM", "New Course Feedback Received"]
    }
};

function switchRole(role) {
    const data = dashboardData[role];
    
    // Update Header
    document.getElementById('dash-title').innerText = data.title;

    // Update Stat Cards
    const grid = document.getElementById('stats-grid');
    grid.innerHTML = data.stats.map(s => `
        <div class="glass-card p-6">
            <p class="text-xs text-gray-500 uppercase font-bold mb-2">${s.label}</p>
            <div class="flex justify-between items-center">
                <h2 class="text-2xl font-bold neon-text">${s.val}</h2>
                <i class="fas ${s.icon} opacity-20 text-xl"></i>
            </div>
        </div>
    `).join('');

    // Update Activity Feed
    const list = document.getElementById('activity-list');
    list.innerHTML = data.activities.map(a => `
        <div class="p-3 border-b border-gray-800 text-sm font-mono text-cyan-100 opacity-80">
            > ${a}
        </div>
    `).join('');

    // Toggle Active Tab Style
    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
    document.getElementById(`btn-${role}`).classList.add('active');
}

// Default View
window.onload = () => switchRole('admin');
