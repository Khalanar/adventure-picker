import time
import random
import events as e
import os


def gameover():
    print ("\n**GAME OVER**")
    e.game_start.run(True)


class Player():
    """
    Class used to create the Player object
    """
    # initialise player weapon is part of next version update
    def __init__(self, gold, weapon, hitpoints):
        self.gold = gold
        self.weapon = weapon
        self.hitpoints = hitpoints

    # Calculates damage from given min and max points.
    # Future version will include list of weapons and damage points
    def calculate_damage_points(self):
        damage = random.randrange(1, 4)
        return damage

    def spend_gold(self, amount):
        self.gold -= amount

    def earn_gold(self, amount):
        self.gold += amount

    def take_damage(self, damage_taken):
        self.hitpoints -= damage_taken
        print(f"You take {damage_taken}p of damage ({self.hitpoints} left)")

        if (self.hitpoints <= 0):
            gameover()


class Event():
    """
    Class used to create new events. Events take in a @text to be displayed
    when run, and a list of possible @next_events. List for next_events
    include the keyword to trigger the event, the event that will be triggered,
    and optionally a function that will run right before running the event.
    Use the optional function to extend functionality for adding resources,
    or starting a combat loop
    """
    def __init__(self):
        pass

    def create_event(self, text, next_events):
        self.text = text
        self.next_events = next_events

    def _evaluate_next_event(self, user_input):
        command_found = False
        for event in self.next_events:
            if (user_input.upper() == event[0].upper()):
                command_found = True
                if(len(event) >= 3):
                    if(callable(event[2])):
                        # print("Extra action to be taken")
                        event[2]()
                    else:
                        event[2].run(True)
                event[1].run(True)

        if (not command_found):
            print(f"{user_input} is not an option")
            self.run(False)

    def run(self, show_text=True):
        os.system('clear')
        print("**********")
        text = f"{self.text}\n\n" if show_text else ""
        print(text)
        inp_options = [event[0] for event in self.next_events]
        action_string = " | ".join([str(opt) for opt in inp_options])

        print(f"What will you do? (type one of the following options):")

        user_input = input(f"{action_string}\n")
        self._evaluate_next_event(user_input)


class Combat():
    """
    Event used to create combat scenarios
    """
    def __init__(self, enemy, player):
        self.enemy = enemy
        self.player = player
        self.combat_delay_seconds = 2

    def run(self, show_text=True):
        print(f"\nYou attack the {self.enemy.name}!")
        while self.enemy.hitpoints > 0:
            time.sleep(self.combat_delay_seconds)
            self.enemy.take_damage(self.player.calculate_damage_points())

            time.sleep(self.combat_delay_seconds)
            self.player.take_damage(self.enemy.damage)

            print("")
        time.sleep(self.combat_delay_seconds/2)
        print(f"You slayed the {self.enemy.name}!")
        time.sleep(self.combat_delay_seconds)


class Enemy():
    """
    Class to create enemies
    """
    def __init__(self, name, hitpoints, damage):
        self.name = name
        self.hitpoints = hitpoints
        self.damage = damage

    def take_damage(self, damage_taken):
        self.hitpoints -= damage_taken
        self.hitpoints = 0 if self.hitpoints < 0 else self.hitpoints
        print(f"{self.name} takes {damage_taken}p",
              f"of damage ({self.hitpoints} left)")
