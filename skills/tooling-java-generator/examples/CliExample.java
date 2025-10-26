package com.example.cli;

import picocli.CommandLine;
import picocli.CommandLine.*;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.concurrent.Callable;

/**
 * Java CLI Example: file line counter with picocli
 * Demonstrates: CLI argument parsing, file I/O, exit codes
 */
@Command(name = "linecount", mixinStandardHelpOptions = true, version = "1.0")
public class CliExample implements Callable<Integer> {

    @Parameters(index = "0", description = "File to count")
    private Path file;

    @Override
    public Integer call() throws IOException {
        long lines = Files.lines(file).count();
        System.out.printf("%d lines in %s%n", lines, file.getFileName());
        return 0;
    }

    public static void main(String[] args) {
        System.exit(new CommandLine(new CliExample()).execute(args));
    }
}
