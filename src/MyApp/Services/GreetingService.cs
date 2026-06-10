namespace MyApp.Services;

public static class GreetingService
{
    public static string GetGreeting(string name)
    {
        return $"Hello, {name}!";
    }
}
