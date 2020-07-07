# A very simple hello world example

How to run

```
./mvnw spring-boot:run
```

Once run send some request with the following

```
watch -n0.1  curl localhost:8081/hello
```

## Findings

* Once sleuth is enabled trace and span ids are added automatically with brave.

```
2020-07-07 16:42:58.506  INFO [hellorest,5f04278215c6ab23dac1b5cd286b1b37,dac1b5cd286b1b37,true] 78524 --- [nio-8081-exec-2] c.e.h.Controller.HelloRestController     : Header 'host' = localhost:8081
2020-07-07 16:42:58.506  INFO [hellorest,5f04278215c6ab23dac1b5cd286b1b37,dac1b5cd286b1b37,true] 78524 --- [nio-8081-exec-2] c.e.h.Controller.HelloRestController     : Header 'user-agent' = curl/7.64.1
2020-07-07 16:42:58.506  INFO [hellorest,5f04278215c6ab23dac1b5cd286b1b37,dac1b5cd286b1b37,true] 78524 --- [nio-8081-exec-2] c.e.h.Controller.HelloRestController     : Header 'accept' = */*
```
Compare logs with `spring.sleuth.enabled=false`

* Wavefront distributed is enabled simply by adding the following dependencies.

```
		<dependency>
			<groupId>com.wavefront</groupId>
			<artifactId>wavefront-spring-boot-starter</artifactId>
		</dependency>
		<dependency>
			<groupId>org.springframework.cloud</groupId>
			<artifactId>spring-cloud-starter-sleuth</artifactId>
		</dependency>
```
* A freemium account is created/cached by a file under `$HOME/.wavefront_freemium`
* If on application properties for actuator is enabled, auto redirect to wavefront url will happen on `localhost:8081/actuator/wavefront`
