# A very simple example of non-HTTP (AMQP) tracing example

How to run

```
# brew install rabbitmq
/usr/local/sbin/rabbitmq-server
cd Producer
./mvnw spring-boot:run
cd Consumer
./mvnw spring-boot:run
```

Once run send some request with the following

```
watch -n0.1  curl localhost:8086
```

## Findings

* non-HTTP protocol tracing is also supported by sleuth > wavefront (should work with Kafka also)
Database query support is not added yet to brave. https://github.com/openzipkin/brave/issues/881

