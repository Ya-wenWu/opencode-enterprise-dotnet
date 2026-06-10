using Xunit;

namespace MyApp.Tests;

public class GreetingServiceTests
{
    [Fact]
    public void GetGreeting_WithValidName_ReturnsFormattedGreeting()
    {
        var result = Services.GreetingService.GetGreeting("World");
        Assert.Equal("Hello, World!", result);
    }
}
