from opentelemetry import trace, metrics
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.resources import Resource, SERVICE_NAME

from backend.core.config import settings


def setup_telemetry():
    resource = Resource(attributes={
        SERVICE_NAME: settings.OTEL_SERVICE_NAME
    })
    
    tracer_provider = TracerProvider(resource=resource)
    span_exporter = OTLPSpanExporter(
        endpoint=f"{settings.OTEL_EXPORTER_OTLP_ENDPOINT}/v1/traces"
    )
    span_processor = BatchSpanProcessor(span_exporter)
    tracer_provider.add_span_processor(span_processor)
    trace.set_tracer_provider(tracer_provider)
    
    metric_exporter = OTLPMetricExporter(
        endpoint=f"{settings.OTEL_EXPORTER_OTLP_ENDPOINT}/v1/metrics"
    )
    metric_reader = PeriodicExportingMetricReader(metric_exporter, export_interval_millis=60000)
    meter_provider = MeterProvider(resource=resource, metric_readers=[metric_reader])
    metrics.set_meter_provider(meter_provider)


def get_tracer(name: str):
    return trace.get_tracer(name)


def get_meter(name: str):
    return metrics.get_meter(name)
