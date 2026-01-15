rooms = {
    "hall": {
        "description": "You are standing in a dimly lit hall. There is one door to the north of you and one to the east",
        "exits": {
            "n": "kitchen",
            "e": {"room": "treasure_room", "locked": True, "key": "key"},
        },
        "items": [],
    },
    "kitchen": {
        "description": "You are in a messy kitchen. There is a strong rotten smell lingering in the air",
        "exits": {"s": "hall"},
        "items": ["key"],
    },
    "treasure_room": {
        "description": "You see piles of gold and jewels. You stuff them in your pockets.",
        "exits": {"w": "hall"},
        "items": [],
    },
}
# directions n,s,w,e
quits = ("quit", "gg")
# game states
current_room = "hall"
running = True
inventory = []


def show_room(room_name):
    room = rooms[room_name]
    print("\n" + room["description"])
    print(f"Exits: {", ".join(room["exits"].keys())}")
    if room["items"]:
        print("You see:", ", ".join(room["items"]))


while running:
    show_room(current_room)
    command = input("> ").lower().strip()

    if command in quits:
        print("Goodbye!")
        running = False
    elif command.startswith("use "):
        item = command.split(" ", 1)[1]
        if item not in inventory:
            print("You dont have that item.")
        used = False

    elif command in rooms[current_room]["exits"]:
        exit_room = rooms[current_room]["exits"][command]
        # locked doors
        if isinstance(exit_room, dict) and exit_room["locked"]:
            print("The door is locked.")

        # normal exit
        else:
            current_room = (
                exit_room["room"] if isinstance(exit_room, dict) else exit_room
            )
    elif command.startswith("take "):
        item = command.split(" ", 1)[1]
        room_items = rooms[current_room]["items"]
        if item in room_items:
            room_items.remove(item)
            inventory.append(item)
            print(f"You picked up the {item}.")
        else:
            print("That item is not here.")
    elif command in ("inventory", "i"):
        if inventory:
            print("You are carrying:", ", ".join(inventory))
        else:
            print("Your inventory is empty.")
    else:
        print("Thats not possible.")
