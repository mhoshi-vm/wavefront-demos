# A very simple example with random errors

## How to run

```
./mvnw spring-boot:run
```

Once run send some request with the following

```
watch -n0.1  curl localhost:8082/hello
```


## Findings
* The code will randomly generate a BAD_REQUEST . This will be logged as error in wavefront

```
	@GetMapping("/hello")
	public ResponseEntity<String> hello (@RequestHeader Map<String, String> header) {
		printAllHeaders(header);
		
		if ((long)(Math.random()*10%10) == 1) {
			return new ResponseEntity<>(HttpStatus.BAD_REQUEST);
		}
		return ResponseEntity.ok("Hello World!");
	}
```