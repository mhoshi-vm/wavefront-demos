An extreme simple tracing sample

```
Demo7 ----> Demo1 (localhost:8081/hello, Spring boot)
       |--> Demo2 (localhost:8082/hello-red, Spring boot with 10% Error rate)
       |--> Demo5 (localhost:5000/, Python w/o proper code handling of trace id)
       |--> Demo6 (localhost:8087/amqp, RabbitMQ example)
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

## Findings

* Wavefront can connect different level of services names (does not have to be the same service name)
* Wavefront will automatically highlight inproper connections (Demo6 > Demo2)
* When multiple apps are connected trace ids are shared and passed
* HTTP headers are added during the tracing
* Non Java codes require, additional coding for propagating traces
