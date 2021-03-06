from components.ai import HostileEnemy
from components import consumable, equippable
from components.equipment import Equipment
from components.fighter import Fighter
from components.inventory import Inventory
from components.level import Level
from entity import Actor, Item

player = Actor(
    char="@",
    color=(255, 255, 255),
    name="Player",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=30, base_defense=1, base_power=2),
    inventory=Inventory(capacity=26),
    level=Level(level_up_base=200)
)

# enemies
orc = Actor(
    char="o",
    color=(63, 127, 63),
    name="Orc",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=10, base_defense=0, base_power=3),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=35)
)

troll = Actor(
    char="T",
    color=(0, 127, 0),
    name="Troll",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=16, base_defense=1, base_power=4),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=100)
)

# scrolls
scroll_char = "?"

confusion_scroll = Item(
    char=scroll_char,
    color=(207, 63, 255),
    name="Confusion Scroll",
    consumable=consumable.ConfusionConsumable(number_of_turns=10)
)

magic_missile_scroll = Item(
    char=scroll_char,
    color=(85, 255, 85),
    name="Magic Missile Scroll",
    consumable=consumable.MagicMissileDamageConsumable(damage=16)
)

lightning_scroll = Item(
    char=scroll_char,
    color=(255, 255, 0),
    name="Lightning Scroll",
    consumable=consumable.LightningDamageConsumable(damage=20, maximum_range=5)
)

fireball_scroll = Item(
    char=scroll_char,
    color=(255, 0, 0),
    name="Fireball Scroll",
    consumable=consumable.FireballDamageConsumable(damage=12, radius=3)
)

# weapons
weapon_char = ")"

dagger = Item(
    char=weapon_char,
    color=(0, 191, 255),
    name="Dagger",
    equippable=equippable.Dagger()
)

sword = Item(
    char=weapon_char,
    color=(0, 191, 255),
    name="Sword",
    equippable=equippable.Sword()
)

# armors
armor_char = "["

leather_armor = Item(
    char=armor_char,
    color=(139, 69, 19),
    name="Leather Armor",
    equippable=equippable.LeatherArmor()
)

chain_mail = Item(
    char=armor_char,
    color=(139, 69, 19),
    name="Chain Mail",
    equippable=equippable.ChainMail()
)

# potions
potion_char = "!"

health_potion = Item(
    char=potion_char,
    color=(127, 0, 255),
    name="Health Potion",
    consumable=consumable.HealingConsumable(amount=4)
)
