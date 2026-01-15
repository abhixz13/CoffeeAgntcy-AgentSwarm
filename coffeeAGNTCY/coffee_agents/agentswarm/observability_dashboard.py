# Copyright AGNTCY Contributors (https://github.com/agntcy)
# SPDX-License-Identifier: Apache-2.0
# AgentSwarm - Real-Time Observability Dashboard
# Demonstrates: Live Metrics, Trace Visualization, Agent Health Monitoring

import os
import sys
import asyncio
import logging
from datetime import datetime
from typing import Dict, Any

# Add parent to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from common.observability import (
    get_trace_store,
    get_metrics_collector,
    get_observability_dashboard,
    mark_startup,
    OTEL_AVAILABLE,
    IOA_AVAILABLE
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("agentswarm.dashboard")

# Initialize FastAPI
app = FastAPI(
    title="AgentSwarm Observability Dashboard",
    description="Real-time monitoring for multi-agent AI system",
    version="1.0.0"
)

# CORS for browser access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# WebSocket connections for live updates
active_connections: list[WebSocket] = []


# =============================================================================
# DASHBOARD HTML (Self-contained for easy demo)
# =============================================================================

DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AgentSwarm Observability Dashboard</title>
    <style>
        :root {
            --bg-primary: #0d1117;
            --bg-secondary: #161b22;
            --bg-card: #21262d;
            --text-primary: #c9d1d9;
            --text-secondary: #8b949e;
            --accent-blue: #58a6ff;
            --accent-green: #3fb950;
            --accent-orange: #d29922;
            --accent-red: #f85149;
            --accent-purple: #a371f7;
            --border: #30363d;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            min-height: 100vh;
        }
        
        .header {
            background: linear-gradient(135deg, #1a1f2e 0%, #0d1117 100%);
            border-bottom: 1px solid var(--border);
            padding: 20px 40px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .header h1 {
            font-size: 24px;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 12px;
        }
        
        .header h1 .logo {
            width: 40px;
            height: 40px;
            background: linear-gradient(135deg, var(--accent-blue), var(--accent-purple));
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
        }
        
        .header .status {
            display: flex;
            gap: 20px;
            align-items: center;
        }
        
        .status-badge {
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 6px 12px;
            background: var(--bg-card);
            border-radius: 20px;
            font-size: 13px;
        }
        
        .status-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            animation: pulse 2s infinite;
        }
        
        .status-dot.healthy { background: var(--accent-green); }
        .status-dot.warning { background: var(--accent-orange); }
        .status-dot.error { background: var(--accent-red); }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        
        .main {
            padding: 30px 40px;
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 20px;
        }
        
        .card {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 20px;
        }
        
        .card.full-width {
            grid-column: span 4;
        }
        
        .card.half-width {
            grid-column: span 2;
        }
        
        .card h2 {
            font-size: 14px;
            font-weight: 500;
            color: var(--text-secondary);
            margin-bottom: 15px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .metric-value {
            font-size: 36px;
            font-weight: 700;
            color: var(--accent-blue);
        }
        
        .metric-label {
            font-size: 12px;
            color: var(--text-secondary);
            margin-top: 5px;
        }
        
        .agent-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 15px;
        }
        
        .agent-card {
            background: var(--bg-secondary);
            border-radius: 8px;
            padding: 15px;
            text-align: center;
        }
        
        .agent-card .icon {
            width: 50px;
            height: 50px;
            margin: 0 auto 10px;
            background: linear-gradient(135deg, var(--accent-blue), var(--accent-purple));
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
        }
        
        .agent-card.crm .icon { background: linear-gradient(135deg, #f97316, #ea580c); }
        .agent-card.knowledge .icon { background: linear-gradient(135deg, #3b82f6, #2563eb); }
        .agent-card.ticket .icon { background: linear-gradient(135deg, #10b981, #059669); }
        .agent-card.escalation .icon { background: linear-gradient(135deg, #ef4444, #dc2626); }
        
        .agent-card h3 {
            font-size: 14px;
            font-weight: 600;
            margin-bottom: 8px;
        }
        
        .agent-stats {
            display: flex;
            justify-content: space-around;
            margin-top: 10px;
            font-size: 12px;
        }
        
        .agent-stats span {
            color: var(--text-secondary);
        }
        
        .agent-stats strong {
            color: var(--accent-green);
        }
        
        .trace-list {
            max-height: 400px;
            overflow-y: auto;
        }
        
        .trace-item {
            background: var(--bg-secondary);
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 10px;
            border-left: 3px solid var(--accent-blue);
        }
        
        .trace-item.error {
            border-left-color: var(--accent-red);
        }
        
        .trace-header {
            display: flex;
            justify-content: space-between;
            margin-bottom: 10px;
        }
        
        .trace-id {
            font-family: monospace;
            color: var(--accent-purple);
        }
        
        .trace-time {
            color: var(--text-secondary);
            font-size: 12px;
        }
        
        .trace-agents {
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
        }
        
        .agent-tag {
            padding: 4px 10px;
            background: var(--bg-card);
            border-radius: 4px;
            font-size: 11px;
            font-weight: 500;
        }
        
        .waterfall {
            margin-top: 15px;
        }
        
        .waterfall-bar {
            height: 24px;
            background: var(--bg-card);
            border-radius: 4px;
            margin-bottom: 8px;
            position: relative;
            overflow: hidden;
        }
        
        .waterfall-fill {
            height: 100%;
            border-radius: 4px;
            display: flex;
            align-items: center;
            padding-left: 10px;
            font-size: 12px;
            font-weight: 500;
        }
        
        .waterfall-fill.crm { background: linear-gradient(90deg, #f97316, #ea580c); }
        .waterfall-fill.knowledge { background: linear-gradient(90deg, #3b82f6, #2563eb); }
        .waterfall-fill.ticket { background: linear-gradient(90deg, #10b981, #059669); }
        .waterfall-fill.escalation { background: linear-gradient(90deg, #ef4444, #dc2626); }
        
        .live-indicator {
            display: flex;
            align-items: center;
            gap: 8px;
            color: var(--accent-green);
            font-size: 13px;
        }
        
        .live-indicator::before {
            content: '';
            width: 8px;
            height: 8px;
            background: var(--accent-green);
            border-radius: 50%;
            animation: pulse 1s infinite;
        }
        
        .token-stats {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }
        
        .token-stat {
            text-align: center;
        }
        
        .token-stat .value {
            font-size: 28px;
            font-weight: 700;
        }
        
        .token-stat.input .value { color: var(--accent-blue); }
        .token-stat.output .value { color: var(--accent-green); }
        
        footer {
            text-align: center;
            padding: 20px;
            color: var(--text-secondary);
            font-size: 12px;
            border-top: 1px solid var(--border);
        }
        
        footer a {
            color: var(--accent-blue);
            text-decoration: none;
        }
    </style>
</head>
<body>
    <header class="header">
        <h1>
            <span class="logo">🤖</span>
            AgentSwarm Observability
        </h1>
        <div class="status">
            <div class="status-badge">
                <span class="status-dot healthy"></span>
                <span>System Healthy</span>
            </div>
            <div class="status-badge">
                <span id="otel-status">OpenTelemetry: Checking...</span>
            </div>
            <div class="live-indicator">LIVE</div>
        </div>
    </header>
    
    <main class="main">
        <!-- Key Metrics -->
        <div class="card">
            <h2>Total Requests</h2>
            <div class="metric-value" id="total-requests">0</div>
            <div class="metric-label">Processed queries</div>
        </div>
        
        <div class="card">
            <h2>Agent Calls</h2>
            <div class="metric-value" id="total-agent-calls">0</div>
            <div class="metric-label">Inter-agent communications</div>
        </div>
        
        <div class="card">
            <h2>Avg Latency</h2>
            <div class="metric-value" id="avg-latency">0<span style="font-size: 18px">ms</span></div>
            <div class="metric-label">Request duration</div>
        </div>
        
        <div class="card">
            <h2>LLM Tokens</h2>
            <div class="metric-value" id="total-tokens">0</div>
            <div class="metric-label">Total consumed</div>
        </div>
        
        <!-- Agent Status -->
        <div class="card full-width">
            <h2>Agent Health & Performance</h2>
            <div class="agent-grid">
                <div class="agent-card crm">
                    <div class="icon">👤</div>
                    <h3>CRM Agent</h3>
                    <div class="agent-stats">
                        <span>Calls: <strong id="crm-calls">0</strong></span>
                        <span>Avg: <strong id="crm-avg">0ms</strong></span>
                    </div>
                </div>
                <div class="agent-card knowledge">
                    <div class="icon">📚</div>
                    <h3>Knowledge Agent</h3>
                    <div class="agent-stats">
                        <span>Calls: <strong id="knowledge-calls">0</strong></span>
                        <span>Avg: <strong id="knowledge-avg">0ms</strong></span>
                    </div>
                </div>
                <div class="agent-card ticket">
                    <div class="icon">🎫</div>
                    <h3>Ticket Agent</h3>
                    <div class="agent-stats">
                        <span>Calls: <strong id="ticket-calls">0</strong></span>
                        <span>Avg: <strong id="ticket-avg">0ms</strong></span>
                    </div>
                </div>
                <div class="agent-card escalation">
                    <div class="icon">🚨</div>
                    <h3>Escalation Agent</h3>
                    <div class="agent-stats">
                        <span>Calls: <strong id="escalation-calls">0</strong></span>
                        <span>Avg: <strong id="escalation-avg">0ms</strong></span>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Recent Traces -->
        <div class="card half-width">
            <h2>Recent Traces (Distributed Tracing)</h2>
            <div class="trace-list" id="trace-list">
                <div class="trace-item">
                    <div class="trace-header">
                        <span class="trace-id">Waiting for traces...</span>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Waterfall View -->
        <div class="card half-width">
            <h2>Latest Request Waterfall</h2>
            <div class="waterfall" id="waterfall">
                <p style="color: var(--text-secondary)">Send a request to see the waterfall visualization</p>
            </div>
        </div>
    </main>
    
    <footer>
        <p>AgentSwarm Multi-Agent System | Powered by <a href="#">AGNTCY Framework</a> + <a href="#">Cisco CIRCUIT AI</a></p>
        <p>OpenTelemetry Distributed Tracing | IOA Observe SDK</p>
    </footer>
    
    <script>
        // WebSocket connection for live updates
        let ws;
        
        function connectWebSocket() {
            ws = new WebSocket(`ws://${window.location.host}/ws`);
            
            ws.onopen = () => {
                console.log('WebSocket connected');
            };
            
            ws.onmessage = (event) => {
                const data = JSON.parse(event.data);
                updateDashboard(data);
            };
            
            ws.onclose = () => {
                console.log('WebSocket disconnected, reconnecting...');
                setTimeout(connectWebSocket, 2000);
            };
        }
        
        function updateDashboard(data) {
            // Update metrics
            if (data.metrics_summary) {
                const metrics = data.metrics_summary;
                document.getElementById('total-requests').textContent = metrics.total_requests || 0;
                document.getElementById('total-agent-calls').textContent = metrics.total_agent_calls || 0;
                
                const tokens = metrics.llm_tokens || {};
                document.getElementById('total-tokens').textContent = 
                    ((tokens.input || 0) + (tokens.output || 0)).toLocaleString();
                
                // Update agent stats
                const agentStats = metrics.agent_stats || {};
                for (const [agent, stats] of Object.entries(agentStats)) {
                    const agentLower = agent.toLowerCase();
                    const callsEl = document.getElementById(`${agentLower}-calls`);
                    const avgEl = document.getElementById(`${agentLower}-avg`);
                    if (callsEl) callsEl.textContent = stats.total_calls || 0;
                    if (avgEl) avgEl.textContent = `${Math.round(stats.avg_duration_ms || 0)}ms`;
                }
            }
            
            // Update average latency
            if (data.aggregated_metrics && data.aggregated_metrics.avg_request_duration_ms) {
                document.getElementById('avg-latency').innerHTML = 
                    `${Math.round(data.aggregated_metrics.avg_request_duration_ms)}<span style="font-size: 18px">ms</span>`;
            }
            
            // Update traces
            if (data.recent_traces && data.recent_traces.length > 0) {
                const traceList = document.getElementById('trace-list');
                traceList.innerHTML = data.recent_traces.map(trace => `
                    <div class="trace-item">
                        <div class="trace-header">
                            <span class="trace-id">${trace.trace_id}</span>
                            <span class="trace-time">${new Date(trace.start_time).toLocaleTimeString()}</span>
                        </div>
                        <div class="trace-agents">
                            ${trace.agent_calls.map(call => 
                                `<span class="agent-tag">${call.agent} (${Math.round(call.duration_ms)}ms)</span>`
                            ).join('')}
                        </div>
                    </div>
                `).join('');
                
                // Update waterfall for latest trace
                const latestTrace = data.recent_traces[0];
                if (latestTrace.agent_calls.length > 0) {
                    const maxDuration = Math.max(...latestTrace.agent_calls.map(c => c.duration_ms));
                    const waterfall = document.getElementById('waterfall');
                    waterfall.innerHTML = latestTrace.agent_calls.map(call => {
                        const width = (call.duration_ms / maxDuration * 100);
                        return `
                            <div class="waterfall-bar">
                                <div class="waterfall-fill ${call.agent.toLowerCase()}" style="width: ${width}%">
                                    ${call.agent} - ${Math.round(call.duration_ms)}ms
                                </div>
                            </div>
                        `;
                    }).join('');
                }
            }
            
            // Update OpenTelemetry status
            if (data.system_health) {
                const otelStatus = document.getElementById('otel-status');
                otelStatus.textContent = `OpenTelemetry: ${data.system_health.otel_enabled ? '✓ Enabled' : '○ Local Only'}`;
            }
        }
        
        // Initial data fetch
        async function fetchInitialData() {
            try {
                const response = await fetch('/api/dashboard');
                const data = await response.json();
                updateDashboard(data);
            } catch (e) {
                console.error('Failed to fetch initial data:', e);
            }
        }
        
        // Polling fallback if WebSocket not available
        function startPolling() {
            setInterval(async () => {
                try {
                    const response = await fetch('/api/dashboard');
                    const data = await response.json();
                    updateDashboard(data);
                } catch (e) {
                    console.error('Polling error:', e);
                }
            }, 2000);
        }
        
        // Initialize
        fetchInitialData();
        connectWebSocket();
        startPolling(); // Fallback
    </script>
</body>
</html>
"""


# =============================================================================
# API ENDPOINTS
# =============================================================================

@app.on_event("startup")
async def startup():
    """Initialize observability on startup."""
    mark_startup()
    logger.info("Observability Dashboard started")
    logger.info(f"OpenTelemetry: {'Enabled' if OTEL_AVAILABLE else 'Not installed'}")
    logger.info(f"IOA Observe SDK: {'Enabled' if IOA_AVAILABLE else 'Not installed'}")


@app.get("/", response_class=HTMLResponse)
async def dashboard():
    """Serve the observability dashboard."""
    return DASHBOARD_HTML


@app.get("/api/dashboard")
async def get_dashboard_data() -> Dict[str, Any]:
    """Get all dashboard data."""
    return await get_observability_dashboard()


@app.get("/api/metrics")
async def get_metrics() -> Dict[str, Any]:
    """Get metrics summary."""
    return get_metrics_collector().get_summary()


@app.get("/api/traces")
async def get_traces(limit: int = 10) -> Dict[str, Any]:
    """Get recent traces."""
    trace_store = get_trace_store()
    return {
        "traces": await trace_store.get_recent_traces(limit),
        "total_count": len(trace_store.traces)
    }


@app.get("/api/health")
async def health_check() -> Dict[str, Any]:
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "otel_enabled": OTEL_AVAILABLE,
        "ioa_enabled": IOA_AVAILABLE
    }


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket for live dashboard updates."""
    await websocket.accept()
    active_connections.append(websocket)
    
    try:
        while True:
            # Send updates every 2 seconds
            data = await get_observability_dashboard()
            await websocket.send_json(data)
            await asyncio.sleep(2)
    except WebSocketDisconnect:
        active_connections.remove(websocket)


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  AGENTSWARM OBSERVABILITY DASHBOARD")
    print("  Real-time Multi-Agent System Monitoring")
    print("=" * 60)
    print(f"\n  Dashboard URL: http://localhost:8080")
    print(f"  API Endpoint:  http://localhost:8080/api/dashboard")
    print(f"\n  OpenTelemetry: {'✓ Enabled' if OTEL_AVAILABLE else '○ Not installed'}")
    print(f"  IOA Observe:   {'✓ Enabled' if IOA_AVAILABLE else '○ Not installed'}")
    print("\n" + "=" * 60 + "\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="info")
