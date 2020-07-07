# Simple demos for understanding tracing in wavefront

## Demos
* demo > Spring hello world
* demo2 > Random error sending 
* demo3 > Sending custom metrics via micrometer
* demo4 > Sending traces via java-agent
* demo5 > Python with wavefront opentracing sdk 
* demo6 > AMQP tracing
* demo7 > Multi-connecting traces
* demo8 > Tracing done via istio
## Glossary
### Trace
A collection of span, which represent the entire flow of the incoming request
### Span
A unit of work, produce throughout the trace
### Headers
Trace and span id's are shared through `x-b3-` headers.
```
x-b3-traceid
x-b3-spanid
x-b3-parentspanid
x-b3-sampled
```
### Propagating Trace/Span
Trace and span ids are not added automatically and needs to be "Propagated". <br>
This includes extracting the trace when arriving from upstream, and reinjecting to the downstream. Without proper coding the connection between application will not properly appear during visualiation
### Wavefront and tracing support
https://docs.wavefront.com/tracing_basics.html#ways-to-send-trace-data-to-wavefront
Key points
* From spring boot 2.3, wavefront support via sleuth or opentracing is added with minimal code modification
* For java application, wavefront provides a java agent to capture and forward all traces with 0 code modication
* For java, .net, python, go wavefront provides an OpenSDK for capturing spans and forwarding to wavefront

### Brave, Slueth and OpenTracing
Brave is a distributed tracing instrumention library developed by OpenZipkin.
Sleuth is additional layer on top of brave to work with spring cloud. Sleuth is compatible with opentracing. OpenTracing is the core of defining the model of distributed tracing
### Service Mesh
Istio/Envoy sidecars will help the propagation of trace and span ids transparent to the code. Currently some discussion is done but will only support 

