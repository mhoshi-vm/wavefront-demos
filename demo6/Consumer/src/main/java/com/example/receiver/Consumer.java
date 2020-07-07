package com.example.receiver;


import java.util.Map;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.amqp.rabbit.annotation.RabbitHandler;
import org.springframework.amqp.rabbit.annotation.RabbitListener;
import org.springframework.messaging.handler.annotation.Headers;
import org.springframework.messaging.handler.annotation.Payload;
import org.springframework.stereotype.Component;

@Component
@RabbitListener(queues = "hello")
public class Consumer {

	private static final Logger LOGGER = LoggerFactory.getLogger(Consumer.class);
	
    @RabbitHandler
    public void receive(@Payload String body, @Headers Map<String,Object> headers) {
		LOGGER.info(String.format(" [x] Received '" + body + headers + "'"));
    }
   
}