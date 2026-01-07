using BattleCityAI.Contracts.GameSessionBase;
using BattleCityAI.StrategyWrapper.CSharp;
using Grpc.Core;
using Grpc.Net.Client;

if (!Environment.UserInteractive || Console.IsInputRedirected)
{
    Thread.Sleep(3000);
}

var strategyUuid = Environment.GetEnvironmentVariable("BCA_STRATEGY_UUID") ?? Guid.Empty.ToString();
Console.WriteLine("Strategy UUID: " + strategyUuid);
Console.WriteLine("Ожидание подключения...");

var channel = GrpcChannel.ForAddress(Environment.GetEnvironmentVariable("BCA_GAMESESSION_SERVER_URL") ?? "http://localhost:6469");
var client = new GameSessionBaseService.GameSessionBaseServiceClient(channel);
var response = await client.ConnectAsync(new ConnectRequest()
{
    StrategyUuid = strategyUuid,
    StrategyVersion = Strategy.StrategyVersion,
    AuthorName = Strategy.AuthorName,
});
Console.WriteLine("Подключено! Ключ аутентификации: " + response.SessionToken);
await Strategy.InitializeAsync(response.TeamId, response.Map, response.Units);

var headers = new Metadata
{
    {"authorization", $"Bearer {response.SessionToken}"}
};

using var duplexPuplex = client.PlaySession(headers);
await foreach (var serverMessage in duplexPuplex.ResponseStream.ReadAllAsync())
{
    //Console.WriteLine($"Receive tick {serverMessage.CurrentTick}");
    var aliveUnits = serverMessage.Teams.First(t => t.Id == response.TeamId).Units.Where(u => u.IsAlive);
    try
    {
        var strategyReaction = await Strategy.ReactAsync(serverMessage, aliveUnits.ToArray());
        await duplexPuplex.RequestStream.WriteAsync(strategyReaction);
    }
    catch (Exception ex)
    {
        Console.WriteLine("[ERR] " + ex.Message);
    }
}
Console.WriteLine("Игровая сессия окончена!");