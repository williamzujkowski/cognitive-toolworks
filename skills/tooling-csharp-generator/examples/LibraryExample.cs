namespace Example.Utils;

/// <summary>
/// C# Library Example: TextAnalyzer utility
/// Demonstrates: records, nullable reference types, LINQ, modern C# features
/// </summary>
public sealed class TextAnalyzer
{
    public record AnalysisResult(int Length, int WordCount, DateTime Analyzed);

    private readonly List<string> _history = new();

    public AnalysisResult Analyze(string text)
    {
        ArgumentException.ThrowIfNullOrWhiteSpace(text);

        _history.Add(text);
        var wordCount = text.Split(' ', StringSplitOptions.RemoveEmptyEntries).Length;

        return new AnalysisResult(text.Length, wordCount, DateTime.UtcNow);
    }

    public IReadOnlyList<string> GetHistory() => _history.AsReadOnly();

    public void Clear() => _history.Clear();
}
