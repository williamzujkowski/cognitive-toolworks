using System.Collections.Concurrent;

namespace Example.Api;

/// <summary>
/// ASP.NET Core Minimal API Example: simple task service
/// Demonstrates: minimal APIs, records, thread-safe collections, endpoints
/// </summary>
public class Program
{
    public record Task(int Id, string Title, bool Done);

    private static readonly ConcurrentDictionary<int, Task> Tasks = new();
    private static int _nextId;

    public static void Main(string[] args)
    {
        var builder = WebApplication.CreateBuilder(args);
        var app = builder.Build();

        app.MapGet("/tasks", () => Results.Ok(Tasks.Values));

        app.MapPost("/tasks", (TaskInput input) =>
        {
            var task = new Task(Interlocked.Increment(ref _nextId), input.Title, false);
            Tasks[task.Id] = task;
            return Results.Created($"/tasks/{task.Id}", task);
        });

        app.Run();
    }

    public record TaskInput(string Title);
}
