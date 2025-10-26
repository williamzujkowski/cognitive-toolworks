using System.CommandLine;

namespace Example.Cli;

/// <summary>
/// C# CLI Example: file line counter
/// Demonstrates: System.CommandLine, file I/O, async/await, exit codes
/// </summary>
public class Program
{
    public static async Task<int> Main(string[] args)
    {
        var fileArg = new Argument<FileInfo>("file", "File to count lines");
        var rootCommand = new RootCommand("Count lines in a file") { fileArg };

        rootCommand.SetHandler(async (FileInfo file) =>
        {
            var lines = await File.ReadAllLinesAsync(file.FullName);
            Console.WriteLine($"{lines.Length} lines in {file.Name}");
        }, fileArg);

        return await rootCommand.InvokeAsync(args);
    }
}
