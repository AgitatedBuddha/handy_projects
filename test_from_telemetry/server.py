import json
import logging

from fastapi import FastAPI, Request
from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response, StreamingResponse


class RequestResponseLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Call the next middleware and wait for the response
        response = await call_next(request)

        # Extract the current span and its trace_id in hex format
        current_span = trace.get_current_span()
        trace_id_hex = format_trace_id(current_span.get_span_context().trace_id)

        # Perform your logging after the response has been sent
        response_body = [chunk async for chunk in response.body_iterator]
        response_body_joined = b"".join(response_body)

        # Log the response body with trace_id
        logging.info(
            json.dumps(
                {
                    "type": "Response",
                    "body": response_body_joined.decode(),
                    "trace_context": {"trace_id": f"0x{trace_id_hex}"},
                }
            )
        )

        # Reconstruct the response
        return Response(
            content=response_body_joined,
            status_code=response.status_code,
            headers=dict(response.headers),
        )


def format_trace_id(trace_id):
    return "{:032x}".format(trace_id)


# Set up the tracer provider and a console exporter
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer_provider().get_tracer(__name__)
trace.get_tracer_provider().add_span_processor(
    SimpleSpanProcessor(ConsoleSpanExporter())
)

app = FastAPI()
app.add_middleware(RequestResponseLoggingMiddleware)

logging.basicConfig(level=logging.INFO)

# Instrument FastAPI app with OpenTelemetry middleware
FastAPIInstrumentor.instrument_app(app, tracer_provider=trace.get_tracer_provider())


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: str):
    with tracer.start_as_current_span("trace_get_item"):
        span = trace.get_current_span()
        span.set_attribute("item_id", item_id)
        return {"item_id": item_id}
