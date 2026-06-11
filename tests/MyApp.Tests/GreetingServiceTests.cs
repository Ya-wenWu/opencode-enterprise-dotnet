using System.Diagnostics.CodeAnalysis;
using Xunit;

namespace MyApp.Tests;

[SuppressMessage("Naming", "CA1707", Justification = "Test names use underscores for readability (MethodName_Scenario_ExpectedBehavior convention)")]
[SuppressMessage("Design", "CA2007", Justification = "Test projects have no SynchronizationContext; ConfigureAwait(false) is unnecessary")]
public class GreetingServiceTests
{
    [Fact]
    public void GetGreeting_WithValidName_ReturnsFormattedGreeting()
    {
        var result = Services.GreetingService.GetGreeting("World");
        Assert.Equal("Hello, World!", result);
    }
}
