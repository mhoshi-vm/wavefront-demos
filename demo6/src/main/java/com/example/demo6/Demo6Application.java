package com.example.demo6;


import java.util.Map;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.http.HttpMethod;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestTemplate;

@SpringBootApplication
public class Demo6Application {

	public static void main(String[] args) {
		SpringApplication.run(Demo6Application.class, args);
	}

}


@RestController
class Demo6Rest{

	private static final Logger LOGGER = LoggerFactory.getLogger(Demo6Rest.class);
		
	
    @Autowired
    RestTemplate restTemplate;
 
    @Bean
    public RestTemplate getRestTemplate() {
        return new RestTemplate();
    }
 

   
    @GetMapping(value="/multi")
    public String MultiRest(@RequestHeader Map<String, String> header) {
		printAllHeaders(header); 
 
        
        String response = (String) restTemplate.exchange("http://localhost:8081/hello", 
                        HttpMethod.GET, null, new ParameterizedTypeReference<String>() {}).getBody();
        String response2 = (String) restTemplate.exchange("http://localhost:8082/hello-red", 
                HttpMethod.GET, null, new ParameterizedTypeReference<String>() {}).getBody();

        String response3 = (String) restTemplate.exchange("http://localhost:5000", 
                HttpMethod.GET, null, new ParameterizedTypeReference<String>() {}).getBody();
        return "Hi...";
    }

	private void printAllHeaders(Map<String, String> headers) {
		headers.forEach((key, value) -> {
			LOGGER.info(String.format("Header '%s' = %s", key, value));
		});
	}
}