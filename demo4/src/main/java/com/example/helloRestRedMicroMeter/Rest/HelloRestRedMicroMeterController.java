package com.example.helloRestRedMicroMeter.Rest;

import java.util.Map;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RestController;

import io.micrometer.core.instrument.Counter;
import io.micrometer.core.instrument.Metrics;

@RestController
public class HelloRestRedMicroMeterController {

	private static final Logger LOGGER = LoggerFactory.getLogger(HelloRestRedMicroMeterController.class);
	
	private Counter counter = Metrics.counter("hello.vistors");

	@GetMapping("/hello-meter")
	public ResponseEntity<String> hello (@RequestHeader Map<String, String> header) {
		printAllHeaders(header);
		counter.increment();
		if ((long)(Math.random()*10%10) == 1) {
			return new ResponseEntity<>(HttpStatus.BAD_REQUEST);
		}
		return ResponseEntity.ok("Hello World!");
	}
	
	private void printAllHeaders(Map<String, String> headers) {
		headers.forEach((key, value) -> {
			LOGGER.info(String.format("Header '%s' = %s", key, value));
		});
	}
}
