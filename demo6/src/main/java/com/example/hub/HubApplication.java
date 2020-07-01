package com.example.hub;


import java.util.Map;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
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
public class HubApplication {

	public static void main(String[] args) {
		SpringApplication.run(HubApplication.class, args);
	}

}


@RestController
class HubController{

	private static final Logger LOGGER = LoggerFactory.getLogger(HubController.class);
		
	@Value("${hub.urls}")
	private String urls;  
	
    @Autowired
    RestTemplate restTemplate;
 
    @Bean
    public RestTemplate getRestTemplate() {
        return new RestTemplate();
    }
   
    @GetMapping(value="/hub")
    public String MultiRest(@RequestHeader Map<String, String> header) {
		printAllHeaders(header); 
		
		for( String url : urls.split(",") )
		{
			LOGGER.info(String.format("URLS = %s", url));
			restTemplate.exchange(url, HttpMethod.GET, null, new ParameterizedTypeReference<String>() {}).getBody();
		}        
        return "Hi...";
    }

	private void printAllHeaders(Map<String, String> headers) {
		headers.forEach((key, value) -> {
			LOGGER.info(String.format("Header '%s' = %s", key, value));
		});
	}
}