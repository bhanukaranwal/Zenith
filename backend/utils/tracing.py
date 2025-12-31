from typing import Dict, Any, Optional
from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode
import functools


def trace_function(span_name: Optional[str] = None):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            tracer = trace.get_tracer(__name__)
            name = span_name or func.__name__
            
            with tracer.start_as_current_span(name) as span:
                try:
                    result = await func(*args, **kwargs)
                    span.set_status(Status(StatusCode.OK))
                    return result
                except Exception as e:
                    span.set_status(Status(StatusCode.ERROR, str(e)))
                    span.record_exception(e)
                    raise
        
        return wrapper
    return decorator


class SpanContext:
    def __init__(self, span_name: str, attributes: Optional[Dict[str, Any]] = None):
        self.span_name = span_name
        self.attributes = attributes or {}
        self.tracer = trace.get_tracer(__name__)
    
    async def __aenter__(self):
        self.span = self.tracer.start_span(self.span_name)
        for key, value in self.attributes.items():
            self.span.set_attribute(key, value)
        return self.span
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.span.set_status(Status(StatusCode.ERROR, str(exc_val)))
            self.span.record_exception(exc_val)
        else:
            self.span.set_status(Status(StatusCode.OK))
        
        self.span.end()
