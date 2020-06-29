"""
Examples of Wavefront Opentracing Python SDK.
@author: Hao Song (songhao@vmware.com)
"""
import time

import opentracing

from wavefront_opentracing_sdk import WavefrontTracer
from wavefront_opentracing_sdk.reporting import CompositeReporter
from wavefront_opentracing_sdk.reporting import ConsoleReporter
from wavefront_opentracing_sdk.reporting import WavefrontSpanReporter

import wavefront_sdk


# pylint: disable=invalid-name
if __name__ == '__main__':
    application_tag = wavefront_sdk.common.ApplicationTags(
        application='example_app',
        service='example_server')
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

    # Create span1, return a newly started and activated Scope.
    scope = tracer.start_active_span(
        operation_name='span1',
        tags=global_tags,
        ignore_active_span=True,
        finish_on_close=True
    )
    span1 = scope.span
    time.sleep(1)

    # Create span2, span3 child of span1.
    span2 = tracer.start_span(
        operation_name='span2',
        references=opentracing.child_of(span1.context),
        tags=[('span2_key', 'span2_val')]
    )
    span2.log_kv({'foo': 'bar'})
    span3 = tracer.start_span(
        operation_name='span3',
        child_of=span1,
        tags=[('span3_key', 'span3_val')]
    )
    time.sleep(2)
    span2.finish()
    time.sleep(1)
    span3.finish()

    # Create span4 follows from span3.
    span4 = tracer.start_span(
        operation_name='span4',
        references=opentracing.follows_from(span3.context),
        tags=[('span4_key', 'span4_val')]
    )
    time.sleep(2)
    span4.finish()

    span5 = tracer.start_span(operation_name='span5')
    time.sleep(1)
    span5.finish()

    time.sleep(1)

    # Close the scope
    scope.close()

    # Close the tracer
    tracer.close()
