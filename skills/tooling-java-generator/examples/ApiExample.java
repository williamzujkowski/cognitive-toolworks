package com.example.api;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicLong;

/**
 * Spring Boot API Example: simple task service
 * Demonstrates: REST endpoints, DTOs, in-memory storage, Spring annotations
 */
@SpringBootApplication
@RestController
@RequestMapping("/tasks")
public class ApiExample {

    record Task(Long id, String title, boolean done) {}

    private final Map<Long, Task> tasks = new ConcurrentHashMap<>();
    private final AtomicLong idGenerator = new AtomicLong();

    @GetMapping
    public List<Task> list() { return List.copyOf(tasks.values()); }

    @PostMapping
    public Task create(@RequestBody Map<String, String> body) {
        Task task = new Task(idGenerator.incrementAndGet(), body.get("title"), false);
        tasks.put(task.id(), task);
        return task;
    }

    public static void main(String[] args) { SpringApplication.run(ApiExample.class, args); }
}
