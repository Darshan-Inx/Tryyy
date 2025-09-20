import random

class Player:
    def __init__(self, name):
        self.name = name
        self.health = 100
        self.gold = 0

    def is_alive(self):
        return self.health > 0

class Monster:
    def __init__(self, name, health, damage):
        self.name = name
        self.health = health
        self.damage = damage

    def is_alive(self):
        return self.health > 0

def encounter(player):
    monsters = [
        Monster("Goblin", 30, 10),
        Monster("Skeleton", 40, 12),
        Monster("Orc", 50, 15)
    ]
    monster = random.choice(monsters)
    print(f"\nA wild {monster.name} appears!")

    while monster.is_alive() and player.is_alive():
        action = input("Do you want to [A]ttack or [R]un? ").lower()
        if action == "a":
            damage = random.randint(5, 20)
            monster.health -= damage
            print(f"You hit {monster.name} for {damage} damage!")
        elif action == "r":
            if random.random() > 0.5:
                print("You successfully ran away!")
                return
            else:
                print("Failed to run!")
        if monster.is_alive():
            player.health -= monster.damage
            print(f"{monster.name} attacks you for {monster.damage} damage!")
    if player.is_alive():
        loot = random.randint(10, 50)
        player.gold += loot
        print(f"You defeated {monster.name} and collected {loot} gold!")
    else:
        print("You have been defeated... Game Over.")

def game():
    name = input("Enter your hero's name: ")
    player = Player(name)

    while player.is_alive():
        print(f"\n{player.name} - Health: {player.health}, Gold: {player.gold}")
        action = input("Do you want to [E]xplore or [Q]uit? ").lower()
        if action == "e":
            encounter(player)
        elif action == "q":
            break

    print(f"Game Over! You collected {player.gold} gold.")

if __name__ == "__main__":
    game()
