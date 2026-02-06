local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Remotes = ReplicatedStorage:WaitForChild("Remotes")
local ClickRemote = Remotes.Click
local BuyRemote = Remotes.BuyMultiplier

-- python dict equivalent
local playerData = {}

local function newPlayerData()
    return {
        coins = 0,
        multiplier = 1
    }
end

Players.PlayerAdded:Connect(function(player)
    playerData[player] = newPlayerData()
end)

Players.PlayerRemoving:Connect(function(player)
    playerData[player] = nil
end)

-- Python: player.click()
ClickRemote.OnServerEvent:Connect(function(player)
    local data = playerData[player]
    if not data then return end

    data.coins += 1 * data.multiplier
end)

-- Python: player.buy_multiplier()
BuyRemote.OnServerEvent:Connect(function(player)
    local data = playerData[player]
    if not data then return end

    local cost = data.multiplier * 10
    if data.coins >= cost then
        data.coins -= cost
        data.multiplier += 1
    end
end)
