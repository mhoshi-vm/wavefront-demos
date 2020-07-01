from flask import Flask, request
from flask import _request_ctx_stack as stack
# Set up sender
from jaeger_client import Tracer, ConstSampler
from jaeger_client.reporter import NullReporter
from jaeger_client.codecs import B3Codec
from opentracing.ext import tags
from opentracing.propagation import Format
from opentracing_instrumentation.request_context import get_current_span,span_in_context
import logging
import sys
from pprint import pprint


# A very basic OpenTracing tracer (with null reporter)
tracer = Tracer(
    one_span_per_rpc=True,
    service_name='hello-world',
    reporter=NullReporter(),
    sampler=ConstSampler(decision=True),
    extra_codecs={Format.HTTP_HEADERS: B3Codec()}
)


app = Flask(__name__)

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.DEBUG)


@app.route("/")
def hello():
    request = stack.top.request
    span_ctx = tracer.extract(Format.HTTP_HEADERS, dict(request.headers))
    rpc_tag = {tags.SPAN_KIND: tags.SPAN_KIND_RPC_SERVER} 
    print(span_ctx)
    print(request.headers)
    with tracer.start_span('hello', child_of=span_ctx , tags=rpc_tag):
        pprint(vars(get_current_span().context))
        return 'Hello World!'
    #return 'Hello World!'


if __name__ == '__main__':
    app.run(debug=True)
