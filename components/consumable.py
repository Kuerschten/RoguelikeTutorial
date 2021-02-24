from __future__ import annotations

from typing import Optional, TYPE_CHECKING

import actions
import color
import components.ai
import components.inventory
from components.base_component import BaseComponent
from exceptions import Impossible
from helper.circle import is_in
from input_handlers import (
    ActionOrHandler,
    AreaRangedAttackHandler,
    SingleRangedAttackHandler,
)

if TYPE_CHECKING:
    from entity import Actor, Item


class Consumable(BaseComponent):
    parent: Item

    def get_action(self, consumer: Actor) -> Optional[ActionOrHandler]:
        """Try to return the action for this item."""
        return actions.ItemAction(consumer, self.parent)

    def activate(self, action: actions.ItemAction) -> None:
        """Invoke this items ability.

        `action` is the context for this activation.
        """
        raise NotImplementedError()

    def consume(self) -> None:
        """Remove the consumed item from its containing inventory."""
        entity = self.parent
        inventory = entity.parent
        if isinstance(inventory, components.inventory.Inventory):
            inventory.items.remove(entity)


class HealingConsumable(Consumable):
    def __init__(self, amount: int):
        self.amount = amount

    def activate(self, action: actions.ItemAction) -> None:
        consumer = action.entity
        amount_recovered = consumer.fighter.heal(self.amount)

        if amount_recovered > 0:
            self.engine.message_log.add_message(
                f"You consume the {self.parent.name}, and recover {amount_recovered} HP!",
                color.health_recovered
            )
            self.consume()
        else:
            raise Impossible(f"Your health is already full.")


class SingleTargetConsumable(Consumable):
    def get_action(self, consumer: Actor) -> SingleRangedAttackHandler:
        self.engine.message_log.add_message(
            "Select a target location.", color.needs_target
        )
        return SingleRangedAttackHandler(
            self.engine,
            callback=lambda xy: actions.ItemAction(consumer, self.parent, xy),
        )

    def activate(self, action: actions.ItemAction) -> None:
        consumer = action.entity
        target = action.target_actor

        if not self.engine.game_map.visible[action.target_xy]:
            raise Impossible("You cannot target an area that you cannot see.")
        if not target:
            raise Impossible("You must select an enemy to target.")
        if target is consumer:
            raise Impossible("You cannot target yourself!")

        self.activate_internal(consumer, target)

        self.consume()

    def activate_internal(self, consumer, target) -> None:
        raise NotImplementedError()


class ConfusionConsumable(SingleTargetConsumable):
    def __init__(self, number_of_turns: int):
        self.number_of_turns = number_of_turns

    def activate_internal(self, consumer, target) -> None:
        self.engine.message_log.add_message(
            f"The eyes of the {target.name} look vacant, as it starts to stumble around!",
            color.status_effect_applied
        )
        target.ai = components.ai.ConfusedEnemy(
            entity=target, previous_ai=target.ai, turns_remaining=self.number_of_turns,
        )


class MagicMissileDamageConsumable(SingleTargetConsumable):
    def __init__(self, damage: int):
        self.damage = damage

    def activate_internal(self, consumer, target) -> None:
        self.engine.message_log.add_message(
            f"The {target.name} is hit by a magic missile, taking {self.damage} damage!"
        )
        target.fighter.take_damage(self.damage)


class AreaTargetConsumable(Consumable):
    def __init__(self, radius: int):
        self.radius = radius

    def get_action(self, consumer: Actor) -> AreaRangedAttackHandler:
        self.engine.message_log.add_message(
            "Select a target location.", color.needs_target
        )
        return AreaRangedAttackHandler(
            self.engine,
            radius=self.radius,
            callback=lambda xy: actions.ItemAction(consumer, self.parent, xy),
        )

    def activate(self, action: actions.ItemAction) -> None:
        consumer = action.entity
        target_xy = action.target_xy

        if not self.engine.game_map.visible[target_xy]:
            raise Impossible("You cannot target an area that you cannot see.")

        targets_hit = False
        for target in self.engine.game_map.actors:
            if is_in(center_xy=(target.x, target.y), radius=self.radius, target_xy=target_xy):
                self.activate_internal(consumer, target)
                targets_hit = True

        if not targets_hit:
            raise Impossible("There are no targets in the radius.")
        self.consume()

    def activate_internal(self, consumer, target) -> None:
        raise NotImplementedError()


class FireballDamageConsumable(AreaTargetConsumable):
    def __init__(self, damage: int, radius: int):
        super().__init__(radius)
        self.damage = damage

    def activate_internal(self, consumer, target) -> None:
        self.engine.message_log.add_message(
            f"The {target.name} is engulfed in a fiery explosion, taking {self.damage} damage!"
        )
        target.fighter.take_damage(self.damage)


class NearestTargetConsumable(Consumable):
    def __init__(self, maximum_range: int):
        self.maximum_range = maximum_range

    def activate(self, action: actions.ItemAction) -> None:
        consumer = action.entity
        target = None
        closest_distance = self.maximum_range + 0.5

        for actor in self.engine.game_map.actors:
            if actor is not consumer and self.parent.gamemap.visible[actor.x, actor.y]:
                distance = consumer.distance(actor.x, actor.y)

                if distance < closest_distance:
                    target = actor
                    closest_distance = distance

        if target:
            self.activate_internal(consumer, target)
            self.consume()
        else:
            raise Impossible("No enemy is close enough.")

    def activate_internal(self, consumer, target):
        raise NotImplementedError()


class LightningDamageConsumable(NearestTargetConsumable):
    def __init__(self, damage: int, maximum_range: int):
        super().__init__(maximum_range)
        self.damage = damage

    def activate_internal(self, consumer, target):
        self.engine.message_log.add_message(
            f"A lighting bolt strikes the {target.name} with a loud thunder, for {self.damage} damage!"
        )
        target.fighter.take_damage(self.damage)
