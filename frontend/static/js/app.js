// Compiled output placeholder. Run `npm run build` in /frontend to regenerate from src/app.ts.
const apiBase = window.localStorage.getItem("siemApiBase") || "http://localhost:8080/api/v1";
let page = 0;
const pageSize = 50;

const statusText = document.getElementById("status-text");
const agentsTable = document.getElementById("agents-table");
const logsTable = document.getElementById("logs-table");
const pageIndicator = document.getElementById("page-indicator");

const searchInput = document.getElementById("search");
const agentFilter = document.getElementById("agent-filter");
const sourceFilter = document.getElementById("source-filter");
const levelFilter = document.getElementById("level-filter");

const refreshAgentsButton = document.getElementById("refresh-agents");
const refreshLogsButton = document.getElementById("refresh-logs");
const prevButton = document.getElementById("prev-page");
const nextButton = document.getElementById("next-page");

const fetchJson = async (path) => {
    const response = await fetch(`${apiBase}${path}`);
    if (!response.ok) {
        throw new Error("Failed request");
    }
    return response.json();
};

const renderAgents = (agents) => {
    agentsTable.innerHTML = "";
    agents.forEach((agent) => {
        const row = document.createElement("tr");
        row.innerHTML = `
            <td>${agent.id}</td>
            <td>${agent.hostname}</td>
            <td>${agent.os_type} ${agent.os_version}</td>
            <td>${agent.last_seen ?? "Never"}</td>
            <td>${agent.log_count}</td>
        `;
        agentsTable.appendChild(row);
    });
};

const renderLogs = (logs) => {
    logsTable.innerHTML = "";
    logs.forEach((log) => {
        const row = document.createElement("tr");
        row.innerHTML = `
            <td>${log.event_time}</td>
            <td>${log.agent_id}</td>
            <td>${log.log_source}</td>
            <td>${log.event_level}</td>
            <td>${log.event_id}</td>
            <td>${log.message}</td>
        `;
        logsTable.appendChild(row);
    });
    statusText.textContent = logs.length ? "Receiving events" : "Awaiting data";
};

const buildLogQuery = () => {
    const params = new URLSearchParams({
        limit: pageSize.toString(),
        offset: (page * pageSize).toString(),
    });

    if (searchInput.value) {
        params.set("search", searchInput.value);
    }
    if (agentFilter.value) {
        params.set("agent_id", agentFilter.value);
    }
    if (sourceFilter.value) {
        params.set("log_source", sourceFilter.value);
    }
    if (levelFilter.value) {
        params.set("event_level", levelFilter.value);
    }

    return `?${params.toString()}`;
};

const loadAgents = async () => {
    const data = await fetchJson("/agents?limit=50&offset=0");
    renderAgents(data);
};

const loadLogs = async () => {
    const data = await fetchJson(`/logs${buildLogQuery()}`);
    renderLogs(data);
    pageIndicator.textContent = `Page ${page + 1}`;
};

refreshAgentsButton.addEventListener("click", () => {
    loadAgents().catch(() => {
        statusText.textContent = "Unable to load agents";
    });
});

refreshLogsButton.addEventListener("click", () => {
    loadLogs().catch(() => {
        statusText.textContent = "Unable to load logs";
    });
});

prevButton.addEventListener("click", () => {
    if (page > 0) {
        page -= 1;
        loadLogs();
    }
});

nextButton.addEventListener("click", () => {
    page += 1;
    loadLogs();
});

loadAgents().catch(() => {
    statusText.textContent = "Unable to load agents";
});
loadLogs().catch(() => {
    statusText.textContent = "Unable to load logs";
});
