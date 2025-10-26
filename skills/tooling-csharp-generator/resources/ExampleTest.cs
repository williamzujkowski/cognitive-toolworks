using Example.Utils;
using FluentAssertions;
using Xunit;

namespace Example.Tests;

/// <summary>
/// xUnit Test Example
/// Demonstrates: modern test structure, FluentAssertions, Theory/InlineData
/// </summary>
public class TextAnalyzerTests
{
    private readonly TextAnalyzer _analyzer = new();

    [Fact]
    public void Analyze_ValidText_ReturnsCorrectMetrics()
    {
        var result = _analyzer.Analyze("Hello world test");

        result.Length.Should().Be(16);
        result.WordCount.Should().Be(3);
        result.Analyzed.Should().BeCloseTo(DateTime.UtcNow, TimeSpan.FromSeconds(1));
    }

    [Theory]
    [InlineData("")]
    [InlineData("   ")]
    public void Analyze_NullOrWhitespace_ThrowsException(string input)
    {
        var act = () => _analyzer.Analyze(input);
        act.Should().Throw<ArgumentException>();
    }
}
