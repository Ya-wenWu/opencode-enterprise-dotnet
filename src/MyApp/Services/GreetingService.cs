namespace MyApp.Services;

internal static class GreetingService
{
    public static string GetGreeting(string name)
    {
        return $"Hello, {name}!";
    }
}
