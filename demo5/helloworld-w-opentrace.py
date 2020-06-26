from flask import Flask

# Set up sender
from wavefront_sdk import WavefrontDirectClient
from wavefront_sdk.common import ApplicationTags
import wavefront_opentracing_sdk
import wavefront_opentracing_sdk.reporting
from wavefront_opentracing_sdk.reporting import CompositeReporter
from wavefront_opentracing_sdk.reporting import ConsoleReporter
from wavefront_opentracing_sdk.reporting import WavefrontSpanReporter
import wavefront_sdk
from wavefront_opentracing_sdk import WavefrontTracer

application_tag = wavefront_sdk.common.ApplicationTags(
    application='demo5',
    service='hello-python')
# Create Wavefront Span Reporter using Wavefront Direct Client.
f = open("wavefront","r")
token = f.read()
f.close()
direct_client = wavefront_sdk.WavefrontDirectClient(
    server="https://wavefront.surf",
    token=token,
    max_queue_size=50000,
    batch_size=10000,
    flush_interval_seconds=5)
direct_reporter = WavefrontSpanReporter(direct_client)


# Create Composite reporter.
# Use ConsoleReporter to output span data to console.
composite_reporter = CompositeReporter(
    direct_reporter, ConsoleReporter())

# Create Tracer with Composite Reporter.
tracer = WavefrontTracer(reporter=composite_reporter,
                         application_tags=application_tag)

global_tags = [('global_key', 'global_val')]

app = Flask(__name__)

@app.route("/")
def hello():
    # Create span1, return a newly started and activated Scope.
    scope = tracer.start_active_span(
        operation_name='span',
        tags=global_tags,
        ignore_active_span=True,
        finish_on_close=True
    )
    span = scope.span
    # Close the scope
    scope.close()
    return "Hello World!"


if __name__ == '__main__':
    app.run(debug=True)
