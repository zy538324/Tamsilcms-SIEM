const apiBase = window.localStorage.getItem("siemApiBase") || "http://localhost:8080/api/v1";
let page = 0;
const pageSize = 50;

const statusText = document.getElementById("status-text") as HTMLSpanElement;
const agentsTable = document.getElementById("agents-table") as HTMLTableSectionElement;
const logsTable = document.getElementById("logs-table") as HTMLTableSectionElement;
const pageIndicator = document.getElementById("page-indicator") as HTMLSpanElement;

const searchInput = document.getElementById("search") as HTMLInputElement;
const agentFilter = document.getElementById("agent-filter") as HTMLInputElement;
const sourceFilter = document.getElementById("source-filter") as HTMLInputElement;
const levelFilter = document.getElementById("level-filter") as HTMLSelectElement;

const refreshAgentsButton = document.getElementById("refresh-agents") as HTMLButtonElement;
const refreshLogsButton = document.getElementById("refresh-logs") as HTMLButtonElement;
const prevButton = document.getElementById("prev-page") as HTMLButtonElement;
const nextButton = document.getElementById("next-page") as HTMLButtonElement;

interface AgentResponse {
    id: string;
    hostname: string;
    os_type: string;
    os_version: string;
    created_at: string;
    last_seen: string | null;
    log_count: string;
}

interface LogResponse {
    id: number;
    agent_id: string;
    log_source: string;
    event_time: string;
    received_at: string;
    event_level: string;
    event_id: string;
    message: string;
}

const fetchJson = async <T>(path: string): Promise<T> => {
    const response = await fetch(`${apiBase}${path}`);
    if (!response.ok) {
        throw new Error("Failed request");
    }
    return response.json() as Promise<T>;
};

const renderAgents = (agents: AgentResponse[]): void => {
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

const renderLogs = (logs: LogResponse[]): void => {
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

const buildLogQuery = (): string => {
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

const loadAgents = async (): Promise<void> => {
    const data = await fetchJson<AgentResponse[]>("/agents?limit=50&offset=0");
    renderAgents(data);
};

const loadLogs = async (): Promise<void> => {
    const data = await fetchJson<LogResponse[]>(`/logs${buildLogQuery()}`);
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
