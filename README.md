# Harry Potter Trading Card Game JSON

This project provides Harry Potter Trading Card Game card data in JSON format for developers to easily use in their projects.

### Contributors
* Tressley Cahill
* Mateusz Koteja


The information presented in these files about Harry Potter, including characters, names and related indicia are trademarks of and © Warner Bros. Entertainment Inc. This project is not produced by, endorsed by, supported by, or affiliated with Warner Bros. Entertainment Inc. All rights reserved.


## Example Cards
### Lesson
```JSON
{
    "number":"113",
    "name":"Care of Magical Creatures",
    "lesson":"Care of Magical Creatures",
    "type":"Lesson",
    "provides":[
        "1",
        "Care of Magical Creatures"
    ],
    "rarity":"Common",
    "artist":[
        "Shanth Enjeti",
        "Melissa Ferreira"
    ]
}
```

### Creature
```JSON
{
    "number":"30",
    "name":"Norbert",
    "lesson":"Care of Magical Creatures",
    "cost":"4",
    "type":"Creature",
    "subTypes":[
        "Dragon",
        "Unique"
    ],
    "description":"To play this card, discard 2 of your Care of Magical Creatures Lessons from play.",
    "dmgEachTurn":"5",
    "health":"3",
    "flavorText":"'They slipped back down the spiral staircase, their hearts as light as their hands, now that Norbert was of was off them.'",
    "rarity":"Rare",
    "artist":"Scott Lewis"
}
```

### Spell
```JSON
{
    "number":"111",
    "name":"Wingardium Leviosa!",
    "lesson":"Charms",
    "cost":"1",
    "type":"Spell",
    "description":"During your opponent's next turn, prevent all damage done to you by your opponent's Creatures.",
    "flavorText":"'The club flew suddenly out of the troll's hand, rose high, high up into the air...'",
    "rarity":"Common",
    "artist":"Ron Spencer"
}
```

### Item
```JSON
{
    "number":"101",
    "name":"Rememberall",
    "lesson":"Transfiguration",
    "cost":"8",
    "type":"Item",
    "description":"During your turn, you may use an Action to put a Lesson card from your discard pile into play.",
    "rarity":"Common",
    "artist":"Marcelo Vignali"
}
```

### Match
```JSON
{
    "number":"26",
    "name":"Slytherin Match",
    "lesson":"Quidditch",
    "cost":"1",
    "type":"Match",
    "subTypes":[
        "Healing"
    ],
    "description":{
        "toWin":"Do 15 damage to your opponent while this card is in play. (That damage doesn't have to be done all at once.)",
        "prize":"The winner may shuffle up to 15 non-Healing cards from his or her discard pile into his or her deck."
    },
    "rarity":"Foil Premium",
    "artist":"Ben Thompson"
}
```

### Adventure
```JSON
{
    "number":"39",
    "name":"4 Privet Drive",
    "type":"Adventure",
    "description":{
        "effect":"Your opponent can't play Spell cards.",
        "toSolve":"Your opponent chooses 6 cards in his or her hand and discards them.",
        "reward":"Your opponent may draw a card."
    },
    "flavorText":"'Harry was used to spiders, because the cupboard under the stairs was full of them, and that was where he slept.'",
    "rarity":"Uncommon",
    "artist":"Michael Koelsch"
}
```

### Character
```JSON
{
    "number":"8",
    "name":"Harry Potter",
    "type":"Character",
    "subTypes":[
        "Wizard",
        "Gryffindor",
        "Unique"
    ],
    "description":"Whenever you use an Action to draw a card, you may draw 2 cards instead of 1.",
    "flavorText":"'There will be books written about Harry — every child in our world will know his name!' - Professor McGonagall",
    "rarity":"Holo-Portrait Premium",
    "artist":"M. Fischer"
}
```