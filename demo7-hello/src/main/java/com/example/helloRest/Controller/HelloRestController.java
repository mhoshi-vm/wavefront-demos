package com.example.helloRest.Controller;

import java.util.Map;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class HelloRestController {

	private static final Logger LOGGER = LoggerFactory.getLogger(HelloRestController.class);
	
	@GetMapping("/hello")
	public ResponseEntity<String> hello (@RequestHeader Map<String, String> header){
		printAllHeaders(header);return
		ResponseEntity.ok("Hello World!");
	}
	
	private void printAllHeaders(Map<String, String> headers) {
		headers.forEach((key, value) -> {
			LOGGER.info(String.format("Header '%s' = %s", key, value));
		});
	}
}
