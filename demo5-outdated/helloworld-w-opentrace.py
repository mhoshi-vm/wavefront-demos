from flask import Flask, request
from flask import _request_ctx_stack as stack
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
from opentracing.ext import tags
from opentracing.propagation import Format
from opentracing_instrumentation.request_context import span_in_context

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

app = Flask(__name__)

#def trace():
#    '''
#    Function decorator that creates opentracing span from incoming b3 headers
#    '''
#    def decorator(f):
#        def wrapper(*args, **kwargs):
#            request = stack.top.request
#            try:
#                # Create a new span context, reading in values (traceid,
#                # spanid, etc) from the incoming x-b3-*** headers.
#                span_ctx = tracer.extract(
#                    Format.HTTP_HEADERS,
#                    dict(request.headers)
#                )
#                # Note: this tag means that the span will *not* be
#                # a child span. It will use the incoming traceid and
#                # spanid. We do this to propagate the headers verbatim.
#                rpc_tag = {tags.SPAN_KIND: tags.SPAN_KIND_RPC_SERVER}
#                span = tracer.start_span(
#                    operation_name='op', child_of=span_ctx, tags=rpc_tag
#                )
#            except Exception as e:
#                # We failed to create a context, possibly due to no
#                # incoming x-b3-*** headers. Start a fresh span.
#                # Note: This is a fallback only, and will create fresh headers,
#                # not propagate headers.
#                span = tracer.start_span('op')
#            with span_in_context(span):
#                r = f(*args, **kwargs)
#                return r
#        wrapper.__name__ = f.__name__
#        return wrapper
#    return decorator


@app.route("/")
#@trace()
def hello():
    request = stack.top.request
    span_ctx = tracer.extract(Format.HTTP_HEADERS, dict(request.headers))
    rpc_tag = {tags.SPAN_KIND: tags.SPAN_KIND_RPC_SERVER} 
    print(span_ctx)
    print(request.headers)
    with tracer.start_span('hello', child_of=span_ctx ):
        return 'Hello World!'
    #return 'Hello World!'


if __name__ == '__main__':
    app.run(debug=True)
