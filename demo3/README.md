# A very simple example with custom metrics

## How to run

```
./mvnw spring-boot:run
```

Once run send some request with the following

```
watch -n0.1  curl localhost:8083/hello-meter
```

## Findings
* Since wavefront enhances micrometer, custom metrics can be easily sent via wavefront

```
	private Counter counter = Metrics.counter("hello.vistors");

	@GetMapping("/hello-meter")
	public ResponseEntity<String> hello (@RequestHeader Map<String, String> header) {
    ...
		counter.increment();
    ...
	}
```