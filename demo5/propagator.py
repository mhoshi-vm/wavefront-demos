from wavefront_opentracing_sdk.propagation.TextMapPropagator import TextMapPropagator

class TextMapPropagatorOpenTracer(TextMapPropagator):
    _BAGGAGE_PREFIX = 'x-b3-'   
