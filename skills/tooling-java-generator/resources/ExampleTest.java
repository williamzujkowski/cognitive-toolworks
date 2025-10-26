package com.example.utils;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.BeforeEach;
import static org.junit.jupiter.api.Assertions.*;

/**
 * JUnit 5 Test Example
 * Demonstrates: modern test structure, assertions, lifecycle methods
 */
class StringMetricsTest {

    private StringMetrics metrics;

    @BeforeEach
    void setUp() {
        metrics = new StringMetrics();
    }

    @Test
    @DisplayName("Should analyze text and return correct metrics")
    void testAnalyze() {
        var result = metrics.analyze("Hello world test");

        assertEquals(16, result.length());
        assertEquals(3, result.wordCount());
        assertNotNull(result.analyzed());
    }

    @Test
    @DisplayName("Should throw exception for blank text")
    void testBlankInput() {
        assertThrows(IllegalArgumentException.class, () -> metrics.analyze(""));
    }
}
