# Copyright AGNTCY Contributors (https://github.com/agntcy)
# SPDX-License-Identifier: Apache-2.0
# AgentSwarm - Enterprise-Grade Observability Module
# Demonstrates: Distributed Tracing, Metrics, Span Context Propagation

import os
import time
import json
import logging
import uuid
import asyncio
from datetime import datetime
from typing import Dict, Any, Optional, List, Callable
from functools import wraps
from contextlib import asynccontextmanager
from dataclasses import dataclass, field, asdict

# OpenTelemetry imports
try:
    from opentelemetry import trace, metrics
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
    from opentelemetry.sdk.metrics import MeterProvider
    from opentelemetry.sdk.metrics.export import ConsoleMetricExporter, PeriodicExportingMetricReader
    from opentelemetry.sdk.resources import Resource, SERVICE_NAME
    from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
    from opentelemetry.trace import Status, StatusCode, SpanKind
    OTEL_AVAILABLE = True
except ImportError:
    OTEL_AVAILABLE = False
    print("[OBSERVABILITY] OpenTelemetry not installed - using local tracing")

# IOA Observe SDK (AGNTCY)
try:
    from ioa_observe.sdk import session_start, session_end
    from ioa_observe.sdk.decorators import agent as ioa_agent, tool as ioa_tool, graph as ioa_graph
    IOA_AVAILABLE = True
except ImportError:
    IOA_AVAILABLE = False
    # Provide no-op decorators
    def ioa_agent(name=None, description=None):
        def decorator(cls):
            return cls
        return decorator
    def ioa_tool(name=None, description=None):
        def decorator(func):
            return func
        return decorator
    def ioa_graph(name=None):
        def decorator(func):
            return func
        return decorator
    def session_start():
        pass
    def session_end():
        pass

logger = logging.getLogger("agentswarm.observability")

# =============================================================================
# TRACE DATA STRUCTURES
# =============================================================================

@dataclass
class SpanData:
    """Represents a single span in a distributed trace."""
    trace_id: str
    span_id: str
    parent_span_id: Optional[str]
    operation_name: str
    service_name: str
    start_time: float
    end_time: Optional[float] = None
    duration_ms: Optional[float] = None
    status: str = "OK"
    attributes: Dict[str, Any] = field(default_factory=dict)
    events: List[Dict[str, Any]] = field(default_factory=list)
    
    def finish(self, status: str = "OK"):
        """Complete the span with timing."""
        self.end_time = time.time()
        self.duration_ms = (self.end_time - self.start_time) * 1000
        self.status = status


@dataclass
class TraceContext:
    """Context for distributed tracing across agents."""
    trace_id: str
    session_id: str
    user_query: str
    start_time: float
    spans: List[SpanData] = field(default_factory=list)
    agent_calls: List[Dict[str, Any]] = field(default_factory=list)
    llm_calls: List[Dict[str, Any]] = field(default_factory=list)
    metrics: Dict[str, Any] = field(default_factory=dict)
    
    def add_span(self, span: SpanData):
        self.spans.append(span)
    
    def add_agent_call(self, agent: str, duration_ms: float, status: str, tokens: int = 0):
        self.agent_calls.append({
            "agent": agent,
            "timestamp": datetime.now().isoformat(),
            "duration_ms": duration_ms,
            "status": status,
            "tokens": tokens
        })
    
    def add_llm_call(self, model: str, duration_ms: float, input_tokens: int, output_tokens: int):
        self.llm_calls.append({
            "model": model,
            "timestamp": datetime.now().isoformat(),
            "duration_ms": duration_ms,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens
        })
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "trace_id": self.trace_id,
            "session_id": self.session_id,
            "user_query": self.user_query[:100],
            "start_time": datetime.fromtimestamp(self.start_time).isoformat(),
            "total_duration_ms": (time.time() - self.start_time) * 1000,
            "span_count": len(self.spans),
            "agent_calls": self.agent_calls,
            "llm_calls": self.llm_calls,
            "metrics": self.metrics
        }


# =============================================================================
# GLOBAL TRACE STORE (In-Memory for Demo)
# =============================================================================

class TraceStore:
    """In-memory store for traces - perfect for demo visualization."""
    
    def __init__(self, max_traces: int = 100):
        self.traces: Dict[str, TraceContext] = {}
        self.max_traces = max_traces
        self._lock = asyncio.Lock()
    
    async def create_trace(self, user_query: str) -> TraceContext:
        """Create a new trace context."""
        async with self._lock:
            trace_id = str(uuid.uuid4())[:8]
            session_id = f"session-{trace_id}"
            
            ctx = TraceContext(
                trace_id=trace_id,
                session_id=session_id,
                user_query=user_query,
                start_time=time.time()
            )
            
            # Cleanup old traces if needed
            if len(self.traces) >= self.max_traces:
                oldest = min(self.traces.keys(), key=lambda k: self.traces[k].start_time)
                del self.traces[oldest]
            
            self.traces[trace_id] = ctx
            
            # Start IOA session if available
            if IOA_AVAILABLE:
                session_start()
            
            return ctx
    
    async def get_trace(self, trace_id: str) -> Optional[TraceContext]:
        """Get a trace by ID."""
        return self.traces.get(trace_id)
    
    async def get_recent_traces(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent traces for dashboard."""
        sorted_traces = sorted(
            self.traces.values(),
            key=lambda t: t.start_time,
            reverse=True
        )[:limit]
        return [t.to_dict() for t in sorted_traces]
    
    async def get_metrics_summary(self) -> Dict[str, Any]:
        """Get aggregated metrics across all traces."""
        if not self.traces:
            return {"message": "No traces recorded yet"}
        
        total_requests = len(self.traces)
        total_agent_calls = sum(len(t.agent_calls) for t in self.traces.values())
        total_llm_calls = sum(len(t.llm_calls) for t in self.traces.values())
        
        # Calculate averages
        durations = [(time.time() - t.start_time) * 1000 for t in self.traces.values()]
        avg_duration = sum(durations) / len(durations) if durations else 0
        
        # Agent call breakdown
        agent_breakdown = {}
        for trace in self.traces.values():
            for call in trace.agent_calls:
                agent = call["agent"]
                if agent not in agent_breakdown:
                    agent_breakdown[agent] = {"count": 0, "total_duration_ms": 0, "errors": 0}
                agent_breakdown[agent]["count"] += 1
                agent_breakdown[agent]["total_duration_ms"] += call["duration_ms"]
                if call["status"] != "OK":
                    agent_breakdown[agent]["errors"] += 1
        
        # Calculate agent averages
        for agent, stats in agent_breakdown.items():
            if stats["count"] > 0:
                stats["avg_duration_ms"] = stats["total_duration_ms"] / stats["count"]
                stats["error_rate"] = (stats["errors"] / stats["count"]) * 100
        
        return {
            "total_requests": total_requests,
            "total_agent_calls": total_agent_calls,
            "total_llm_calls": total_llm_calls,
            "avg_request_duration_ms": round(avg_duration, 2),
            "agent_breakdown": agent_breakdown,
            "timestamp": datetime.now().isoformat()
        }


# Global trace store
_trace_store: Optional[TraceStore] = None

def get_trace_store() -> TraceStore:
    """Get or create the global trace store."""
    global _trace_store
    if _trace_store is None:
        _trace_store = TraceStore()
    return _trace_store


# =============================================================================
# OPENTELEMETRY SETUP
# =============================================================================

_tracer: Optional[Any] = None
_meter: Optional[Any] = None

def setup_opentelemetry(service_name: str = "agentswarm"):
    """
    Initialize OpenTelemetry tracing and metrics.
    
    Exports to:
    - Console (always, for demo visibility)
    - OTLP endpoint (if OTLP_HTTP_ENDPOINT is set - for Jaeger/Grafana)
    
    Set OTLP_HTTP_ENDPOINT=http://localhost:4318 to export to Docker stack.
    """
    global _tracer, _meter
    
    if not OTEL_AVAILABLE:
        logger.warning("OpenTelemetry not available - using local tracing only")
        return
    
    # Create resource with service info
    resource = Resource.create({
        SERVICE_NAME: service_name,
        "service.version": "1.0.0",
        "service.namespace": "agentswarm",
        "deployment.environment": "hackathon-demo"
    })
    
    # Setup tracer
    tracer_provider = TracerProvider(resource=resource)
    
    # Add console exporter for demo visibility (always enabled)
    console_exporter = ConsoleSpanExporter()
    tracer_provider.add_span_processor(BatchSpanProcessor(console_exporter))
    
    # Check for OTLP endpoint (Docker observability stack)
    otlp_endpoint = os.getenv("OTLP_HTTP_ENDPOINT", "http://localhost:4318")
    
    try:
        from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
        from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
        
        # OTLP Trace Exporter -> Jaeger
        otlp_trace_exporter = OTLPSpanExporter(endpoint=f"{otlp_endpoint}/v1/traces")
        tracer_provider.add_span_processor(BatchSpanProcessor(otlp_trace_exporter))
        logger.info(f"[OTEL] Trace exporter configured: {otlp_endpoint}/v1/traces")
        
        # OTLP Metrics Exporter -> Prometheus via OTEL Collector
        otlp_metric_exporter = OTLPMetricExporter(endpoint=f"{otlp_endpoint}/v1/metrics")
        metric_reader = PeriodicExportingMetricReader(
            otlp_metric_exporter,
            export_interval_millis=10000  # Export every 10 seconds
        )
        logger.info(f"[OTEL] Metrics exporter configured: {otlp_endpoint}/v1/metrics")
        
    except ImportError:
        logger.warning("[OTEL] OTLP exporters not available - using console only")
        metric_reader = PeriodicExportingMetricReader(
            ConsoleMetricExporter(),
            export_interval_millis=60000
        )
    except Exception as e:
        logger.warning(f"[OTEL] Could not configure OTLP exporters: {e}")
        metric_reader = PeriodicExportingMetricReader(
            ConsoleMetricExporter(),
            export_interval_millis=60000
        )
    
    trace.set_tracer_provider(tracer_provider)
    _tracer = trace.get_tracer(__name__)
    
    # Setup metrics
    meter_provider = MeterProvider(resource=resource, metric_readers=[metric_reader])
    metrics.set_meter_provider(meter_provider)
    _meter = metrics.get_meter(__name__)
    
    logger.info(f"[OTEL] OpenTelemetry initialized for {service_name}")
    logger.info(f"[OTEL] View traces at: http://localhost:16686 (Jaeger)")
    logger.info(f"[OTEL] View metrics at: http://localhost:3001 (Grafana)")


def get_tracer():
    """Get the OpenTelemetry tracer."""
    global _tracer
    if _tracer is None and OTEL_AVAILABLE:
        setup_opentelemetry()
    return _tracer


def get_meter():
    """Get the OpenTelemetry meter."""
    global _meter
    if _meter is None and OTEL_AVAILABLE:
        setup_opentelemetry()
    return _meter


# =============================================================================
# TRACING DECORATORS
# =============================================================================

def traced_agent(agent_name: str):
    """
    Decorator to add distributed tracing to agent methods.
    
    Usage:
        @traced_agent("knowledge")
        async def process(self, query: str) -> str:
            ...
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            span_id = str(uuid.uuid4())[:8]
            trace_id = kwargs.pop("trace_id", str(uuid.uuid4())[:8])
            parent_span_id = kwargs.pop("parent_span_id", None)
            
            # Create span data
            span = SpanData(
                trace_id=trace_id,
                span_id=span_id,
                parent_span_id=parent_span_id,
                operation_name=f"{agent_name}.{func.__name__}",
                service_name=f"agentswarm.{agent_name}",
                start_time=start_time,
                attributes={
                    "agent.name": agent_name,
                    "agent.operation": func.__name__
                }
            )
            
            # OpenTelemetry span
            otel_span = None
            tracer = get_tracer()
            if tracer:
                otel_span = tracer.start_span(
                    f"{agent_name}.{func.__name__}",
                    kind=SpanKind.INTERNAL,
                    attributes={
                        "agent.name": agent_name,
                        "agent.type": "specialist"
                    }
                )
            
            try:
                result = await func(*args, **kwargs)
                span.finish("OK")
                
                if otel_span:
                    otel_span.set_status(Status(StatusCode.OK))
                    otel_span.set_attribute("response.length", len(str(result)))
                    otel_span.end()
                
                # Log for demo visibility
                logger.info(f"[TRACE] {agent_name}.{func.__name__} completed in {span.duration_ms:.2f}ms")
                
                return result
                
            except Exception as e:
                span.finish("ERROR")
                span.attributes["error"] = str(e)
                
                if otel_span:
                    otel_span.set_status(Status(StatusCode.ERROR, str(e)))
                    otel_span.record_exception(e)
                    otel_span.end()
                
                logger.error(f"[TRACE] {agent_name}.{func.__name__} failed: {e}")
                raise
        
        return wrapper
    return decorator


def traced_llm_call(model_name: str = "unknown"):
    """
    Decorator to trace LLM calls with token counting.
    
    Usage:
        @traced_llm_call("gpt-4o-mini")
        async def invoke(self, prompt: str) -> str:
            ...
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            
            tracer = get_tracer()
            otel_span = None
            if tracer:
                otel_span = tracer.start_span(
                    f"llm.{model_name}",
                    kind=SpanKind.CLIENT,
                    attributes={
                        "llm.model": model_name,
                        "llm.provider": "circuit" if "circuit" in model_name.lower() else "openai"
                    }
                )
            
            try:
                result = await func(*args, **kwargs)
                duration_ms = (time.time() - start_time) * 1000
                
                # Estimate tokens (rough estimate for demo)
                input_text = str(args) + str(kwargs)
                output_text = str(result)
                input_tokens = len(input_text) // 4
                output_tokens = len(output_text) // 4
                
                if otel_span:
                    otel_span.set_attribute("llm.input_tokens", input_tokens)
                    otel_span.set_attribute("llm.output_tokens", output_tokens)
                    otel_span.set_attribute("llm.duration_ms", duration_ms)
                    otel_span.set_status(Status(StatusCode.OK))
                    otel_span.end()
                
                logger.info(f"[LLM] {model_name}: {input_tokens}→{output_tokens} tokens, {duration_ms:.0f}ms")
                
                return result
                
            except Exception as e:
                if otel_span:
                    otel_span.set_status(Status(StatusCode.ERROR, str(e)))
                    otel_span.record_exception(e)
                    otel_span.end()
                raise
        
        return wrapper
    return decorator


# =============================================================================
# METRICS COLLECTION
# =============================================================================

class MetricsCollector:
    """Collects and exposes metrics for the multi-agent system."""
    
    def __init__(self):
        self.request_count = 0
        self.agent_call_counts: Dict[str, int] = {}
        self.agent_durations: Dict[str, List[float]] = {}
        self.llm_token_counts: Dict[str, int] = {"input": 0, "output": 0}
        self.error_counts: Dict[str, int] = {}
        
        # OpenTelemetry metrics
        meter = get_meter()
        if meter:
            self._request_counter = meter.create_counter(
                "agentswarm.requests",
                description="Total requests processed"
            )
            self._agent_duration_histogram = meter.create_histogram(
                "agentswarm.agent.duration",
                description="Agent call duration in ms"
            )
            self._token_counter = meter.create_counter(
                "agentswarm.llm.tokens",
                description="LLM tokens used"
            )
    
    def record_request(self):
        """Record a new request."""
        self.request_count += 1
        if hasattr(self, '_request_counter'):
            self._request_counter.add(1)
    
    def record_agent_call(self, agent_name: str, duration_ms: float, success: bool = True):
        """Record an agent call."""
        if agent_name not in self.agent_call_counts:
            self.agent_call_counts[agent_name] = 0
            self.agent_durations[agent_name] = []
        
        self.agent_call_counts[agent_name] += 1
        self.agent_durations[agent_name].append(duration_ms)
        
        if not success:
            if agent_name not in self.error_counts:
                self.error_counts[agent_name] = 0
            self.error_counts[agent_name] += 1
        
        if hasattr(self, '_agent_duration_histogram'):
            self._agent_duration_histogram.record(duration_ms, {"agent": agent_name})
    
    def record_llm_tokens(self, input_tokens: int, output_tokens: int):
        """Record LLM token usage."""
        self.llm_token_counts["input"] += input_tokens
        self.llm_token_counts["output"] += output_tokens
        
        if hasattr(self, '_token_counter'):
            self._token_counter.add(input_tokens, {"type": "input"})
            self._token_counter.add(output_tokens, {"type": "output"})
    
    def get_summary(self) -> Dict[str, Any]:
        """Get metrics summary for dashboard."""
        agent_stats = {}
        for agent, durations in self.agent_durations.items():
            if durations:
                agent_stats[agent] = {
                    "total_calls": self.agent_call_counts.get(agent, 0),
                    "avg_duration_ms": sum(durations) / len(durations),
                    "min_duration_ms": min(durations),
                    "max_duration_ms": max(durations),
                    "p95_duration_ms": sorted(durations)[int(len(durations) * 0.95)] if len(durations) > 1 else durations[0],
                    "error_count": self.error_counts.get(agent, 0)
                }
        
        return {
            "total_requests": self.request_count,
            "total_agent_calls": sum(self.agent_call_counts.values()),
            "llm_tokens": self.llm_token_counts,
            "agent_stats": agent_stats,
            "timestamp": datetime.now().isoformat()
        }


# Global metrics collector
_metrics_collector: Optional[MetricsCollector] = None

def get_metrics_collector() -> MetricsCollector:
    """Get or create the global metrics collector."""
    global _metrics_collector
    if _metrics_collector is None:
        _metrics_collector = MetricsCollector()
    return _metrics_collector


# =============================================================================
# OBSERVABILITY DASHBOARD DATA
# =============================================================================

async def get_observability_dashboard() -> Dict[str, Any]:
    """
    Get comprehensive observability data for dashboard display.
    This is the main endpoint for the demo dashboard.
    """
    trace_store = get_trace_store()
    metrics = get_metrics_collector()
    
    return {
        "title": "AgentSwarm Observability Dashboard",
        "timestamp": datetime.now().isoformat(),
        "system_health": {
            "status": "HEALTHY",
            "uptime_seconds": time.time() - _startup_time if _startup_time else 0,
            "otel_enabled": OTEL_AVAILABLE,
            "ioa_enabled": IOA_AVAILABLE
        },
        "metrics_summary": metrics.get_summary(),
        "recent_traces": await trace_store.get_recent_traces(10),
        "aggregated_metrics": await trace_store.get_metrics_summary()
    }


# Startup time tracking
_startup_time: Optional[float] = None

def mark_startup():
    """Mark the system startup time."""
    global _startup_time
    _startup_time = time.time()


# =============================================================================
# VISUAL TRACE OUTPUT (FOR DEMO)
# =============================================================================

def format_trace_for_display(trace_ctx: TraceContext) -> str:
    """
    Format a trace for visual display in the demo.
    Creates ASCII art representation of the distributed trace.
    """
    output = []
    output.append("\n" + "=" * 60)
    output.append("         DISTRIBUTED TRACE VISUALIZATION")
    output.append("         OpenTelemetry + AGNTCY Observe SDK")
    output.append("=" * 60)
    output.append(f"\nTrace ID: {trace_ctx.trace_id}")
    output.append(f"Session:  {trace_ctx.session_id}")
    output.append(f"Query:    {trace_ctx.user_query[:50]}...")
    output.append("")
    
    # Timeline visualization
    output.append("EXECUTION TIMELINE (Waterfall View):")
    output.append("-" * 60)
    
    total_duration = (time.time() - trace_ctx.start_time) * 1000
    
    for i, call in enumerate(trace_ctx.agent_calls):
        # Calculate relative position
        pct = (call["duration_ms"] / total_duration * 100) if total_duration > 0 else 0
        bar_len = int(pct / 2)  # Scale to 50 chars max
        bar = "█" * bar_len + "░" * (50 - bar_len)
        
        status_icon = "✓" if call["status"] == "OK" else "✗"
        output.append(f"[{i+1}] {call['agent']:12} |{bar}| {call['duration_ms']:>6.1f}ms {status_icon}")
    
    output.append("-" * 60)
    output.append(f"Total Duration: {total_duration:.1f}ms")
    output.append("")
    
    # Span tree visualization
    if trace_ctx.spans:
        output.append("SPAN TREE:")
        output.append("-" * 60)
        for span in trace_ctx.spans:
            indent = "  " if span.parent_span_id else ""
            output.append(f"{indent}├─ {span.operation_name}")
            output.append(f"{indent}│  └─ {span.duration_ms:.1f}ms | {span.status}")
    
    output.append("")
    
    # LLM calls
    if trace_ctx.llm_calls:
        output.append("LLM INVOCATIONS:")
        output.append("-" * 60)
        total_input = sum(c["input_tokens"] for c in trace_ctx.llm_calls)
        total_output = sum(c["output_tokens"] for c in trace_ctx.llm_calls)
        for call in trace_ctx.llm_calls:
            output.append(f"  • {call['model']}: {call['input_tokens']}→{call['output_tokens']} tokens ({call['duration_ms']:.0f}ms)")
        output.append(f"  Total: {total_input}→{total_output} tokens")
    
    output.append("")
    output.append("=" * 60)
    
    return "\n".join(output)


# =============================================================================
# EXPORT FOR EASY IMPORTING
# =============================================================================

__all__ = [
    # Core classes
    "TraceContext",
    "SpanData",
    "TraceStore",
    "MetricsCollector",
    
    # Decorators
    "traced_agent",
    "traced_llm_call",
    "ioa_agent",
    "ioa_tool",
    "ioa_graph",
    
    # Functions
    "get_trace_store",
    "get_metrics_collector",
    "get_observability_dashboard",
    "setup_opentelemetry",
    "format_trace_for_display",
    "mark_startup",
    "session_start",
    "session_end",
    
    # Flags
    "OTEL_AVAILABLE",
    "IOA_AVAILABLE"
]
