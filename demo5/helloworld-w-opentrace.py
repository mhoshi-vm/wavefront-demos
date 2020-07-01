from flask import Flask,request

# Set up sender
import opentracing

from wavefront_opentracing_sdk import WavefrontTracer
from wavefront_opentracing_sdk import span_context
from wavefront_opentracing_sdk.reporting import CompositeReporter
from wavefront_opentracing_sdk.reporting import ConsoleReporter
from wavefront_opentracing_sdk.reporting import WavefrontSpanReporter

import wavefront_sdk

import uuid

app = Flask(__name__)

@app.route("/")
def hello():
    _BAGGAGE_PREFIX = 'x-b3-'
    _TRACE_ID = _BAGGAGE_PREFIX + 'traceid'
    _SPAN_ID = _BAGGAGE_PREFIX + 'spanid'
    _SAMPLE = _BAGGAGE_PREFIX + 'sample'

    trace_id = None
    span_id = None
    sampling = None
    baggage = {}
    for key, val in dict(request.headers).items():
        print(key)
        key = key.lower()
        if key == _TRACE_ID:
            trace_id = val
        elif key == _SPAN_ID:
            span_id = val
        elif key == _SAMPLE:
            sampling = bool(val == 'True')
        elif key.startswith(_BAGGAGE_PREFIX):
            baggage.update({strip_prefix(_BAGGAGE_PREFIX, key): val}) 
    if trace_id is None or span_id is None:
       span_ctx=None    
    else:
       span_ctx = span_context.WavefrontSpanContext(trace_id, span_id, baggage,
                                                 sampling)
    # Create span1, return a newly started and activated Scope.
    with tracer.start_active_span('hello', child_of=span_ctx, ignore_active_span=True, finish_on_close=True):
      return "Hello World!"

def strip_prefix(prefix, key):
    """
    Strip the prefix of baggage items.
    :param prefix: Prefix to be stripped.
    :type prefix: str
    :param key: Baggage item to be striped
    :type key: str
    :return: Striped baggage item
    :rtype: str
    """
    return key[len(prefix):]


if __name__ == '__main__':
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


    app.run(debug=True)
