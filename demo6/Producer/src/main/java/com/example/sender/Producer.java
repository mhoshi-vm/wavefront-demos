package com.example.sender;

import org.springframework.amqp.core.Queue;
import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.stereotype.Component;

@Component
public class Producer{

    @Bean
    public Queue hello() {
        return new Queue("hello");
    }	
	
    @Autowired
    private RabbitTemplate template;

    @Autowired
    private Queue queue;
    
    public void send() {
        String message = "Hello World!";
        this.template.convertAndSend(queue.getName(), message);
        System.out.println(" [x] Sent '" + message + "'");
    }
}