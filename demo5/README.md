# A very simple example of python code using wavefront opensdk

## How to run
```
virtualenv env1
source env1/bin/activate
pip install -r requirments.txt
python helloworld-w-opentrace.py
```
Once run send some request with the following

```
watch -n0.1  curl localhost:5000
```

## Findings
* Using wavefront opentracing sdk, you need to code a tracer object to connect to wavefront
* Tracing will be added by adding a `tracer.start_active_span` method to where you want to trace (vice versa, will not be traced without this)

```
    # Create span1, return a newly started and activated Scope.
    with tracer.start_active_span('hello', child_of=span_ctx, ignore_active_span=True, finish_on_close=True):
      return "Hello World!"
```

* For extracting incoming http request a manual code to parse the `x-b3-` headers are needed

```
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
        print(val)
        key = key.lower()
        if key == _TRACE_ID:
            trace_id = uuid.UUID(val.zfill(32))
        elif key == _SPAN_ID:
            span_id = uuid.UUID(val.zfill(32))
        elif key == _SAMPLE:
            sampling = bool(val == 'True')
        elif key.startswith(_BAGGAGE_PREFIX):
            baggage.update({strip_prefix(_BAGGAGE_PREFIX, key): val}) 
    if trace_id is None or span_id is None:
       span_ctx=None    
    else:
       span_ctx = span_context.WavefrontSpanContext(trace_id, span_id, baggage,
                                                 sampling)
```
