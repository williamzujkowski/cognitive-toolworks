package com.example.utils;

import java.time.Instant;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/**
 * Java Library Example: StringMetrics utility
 * Demonstrates: immutability, record types, collections, modern Java features
 */
public final class StringMetrics {

    public record Metrics(int length, int wordCount, Instant analyzed) {}

    private final List<String> history = new ArrayList<>();

    public Metrics analyze(String text) {
        if (text == null || text.isBlank()) {
            throw new IllegalArgumentException("Text cannot be null or blank");
        }

        history.add(text);
        int wordCount = text.split("\\s+").length;

        return new Metrics(text.length(), wordCount, Instant.now());
    }

    public List<String> getHistory() {
        return Collections.unmodifiableList(history);
    }
}
