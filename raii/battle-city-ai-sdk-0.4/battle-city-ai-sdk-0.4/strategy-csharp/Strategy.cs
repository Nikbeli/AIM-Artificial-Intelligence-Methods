using BattleCityAI.Contracts.GameSessionBase;

namespace BattleCityAI.StrategyWrapper.CSharp;

/// <summary>
/// Описание стратегии.
/// </summary>
internal static class Strategy
{
    public const int StrategyVersion = 1;

    public const string AuthorName = "John Doe";

    public static Task InitializeAsync(uint teamId, GameMapInfo map, IReadOnlyCollection<UnitInfo> units)
    {
        return Task.CompletedTask;
    }

    public static Task<StrategyReaction> ReactAsync(GameFieldState state, IReadOnlyCollection<UnitInfo> aliveUnits)
    {
        return Task.FromResult(new StrategyReaction()
        {
            CurrentTick = state.CurrentTick,
            Units = {
                // Очень "простая" стратегия: редко поворачиваться, всегда двигаться и стрелять.
                aliveUnits.Select(ou => new StrategyReactionUnit()
                {
                    Id = ou.Id,
                    Rotation = Random.Shared.NextDouble() < 0.94 ? ou.PositionAndSpeed.Rotation : (RotationType)(((int)ou.PositionAndSpeed.Rotation + 1) % 4),
                    WillMove = true,
                    WillShoot = true,
                })
            },
        });
    }
}
