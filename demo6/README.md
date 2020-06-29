An extreme simple tracing sample

```
Demo6 ----> Demo1 (localhost:8081/hello, Spring boot)
       |--> Demo2 (localhost:8082/hello-red, Spring boot with 10% Error rate)
       |--> Demo3 (localhost:5000/, Python w/o proper code handling of trace id)
```

Look at logs at Demo6

```
2020-06-29 15:38:14.453  INFO [,5ef98c56350746730007aa298753a7f6,0007aa298753a7f6,true] 64055 --- [nio-8086-exec-4] com.example.demo6.Demo6Rest              : Header 'host' = localhost:8086
2020-06-29 15:38:14.453  INFO [,5ef98c56350746730007aa298753a7f6,0007aa298753a7f6,true] 64055 --- [nio-8086-exec-4] com.example.demo6.Demo6Rest              : Header 'user-agent' = curl/7.64.1
2020-06-29 15:38:14.453  INFO [,5ef98c56350746730007aa298753a7f6,0007aa298753a7f6,true] 64055 --- [nio-8086-exec-4] com.example.demo6.Demo6Rest              : Header 'accept' = */*
```

Compare that with Demo1

```
2020-06-29 15:38:14.456  INFO [,5ef98c56350746730007aa298753a7f6,be989a7adda54be9,true] 64052 --- [nio-8081-exec-4] c.e.h.Controller.HelloRestController     : Header 'accept' = text/plain, application/json, application/*+json, */*
2020-06-29 15:38:14.456  INFO [,5ef98c56350746730007aa298753a7f6,be989a7adda54be9,true] 64052 --- [nio-8081-exec-4] c.e.h.Controller.HelloRestController     : Header 'x-b3-traceid' = 5ef98c56350746730007aa298753a7f6
2020-06-29 15:38:14.456  INFO [,5ef98c56350746730007aa298753a7f6,be989a7adda54be9,true] 64052 --- [nio-8081-exec-4] c.e.h.Controller.HelloRestController     : Header 'x-b3-spanid' = 9aab85af51d2284f
2020-06-29 15:38:14.456  INFO [,5ef98c56350746730007aa298753a7f6,be989a7adda54be9,true] 64052 --- [nio-8081-exec-4] c.e.h.Controller.HelloRestController     : Header 'x-b3-parentspanid' = 0007aa298753a7f6
2020-06-29 15:38:14.456  INFO [,5ef98c56350746730007aa298753a7f6,be989a7adda54be9,true] 64052 --- [nio-8081-exec-4] c.e.h.Controller.HelloRestController     : Header 'x-b3-sampled' = 1
2020-06-29 15:38:14.456  INFO [,5ef98c56350746730007aa298753a7f6,be989a7adda54be9,true] 64052 --- [nio-8081-exec-4] c.e.h.Controller.HelloRestController     : Header 'user-agent' = Java/14.0.1
2020-06-29 15:38:14.456  INFO [,5ef98c56350746730007aa298753a7f6,be989a7adda54be9,true] 64052 --- [nio-8081-exec-4] c.e.h.Controller.HelloRestController     : Header 'host' = localhost:8081
2020-06-29 15:38:14.456  INFO [,5ef98c56350746730007aa298753a7f6,be989a7adda54be9,true] 64052 --- [nio-8081-exec-4] c.e.h.Controller.HelloRestController     : Header 'connection' = keep-alive
```

You will see that trace_id `5ef98c56350746730007aa298753a7f6` is same among 2 services. <br>
The span id between services. Also in the http header at Demo1, the following http headers are added

```
x-b3-traceid
x-b3-spanid
x-b3-parentspanid
x-b3-sampled
```

However since we have not coded Demo6 properly, the python code will not share the code properly and generates a different trace id, thus leading to a service being isolated. The following logs show it is using trace_id `1bd8c07c-b9d3-11ea-8bb8-acde48001122`

```
INFO:werkzeug:127.0.0.1 - - [29/Jun/2020 15:38:14] "GET / HTTP/1.1" 200 -
INFO:wavefront_opentracing_sdk.reporting.console:Finished span: sampling=True "span" source="unknown" traceId=1bd8c07c-b9d3-11ea-8bb8-acde48001122 spanId=1bd8c07c-b9d3-11ea-8bb8-acde48001122 "global_key"="global_val" "application"="demo5" "service"="hello-python" "cluster"="none" "shard"="none" "component"="none" 1593412694464 0
```

## Notable limitations

At this point of writing, the wavefront python SDK does not support extract(nor inject) incoming(nor outgoing) traces.

https://github.com/wavefrontHQ/wavefront-opentracing-sdk-python/blob/master/wavefront_opentracing_sdk/propagation/propagator.py#L12-L21

## Learnings

* Wavefront can connect different level of services names (does not have to be the same service name)
* Wavefront will automatically highlight inproper connections (Demo6 > Demo2)
* When multiple apps are connected trace ids are shared and passed
* HTTP headers are added during the tracing
* The python service will not be connected as it currently is not 
* Connecting multi language applications is not yet a common use case 