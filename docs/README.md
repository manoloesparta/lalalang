# La La Lang's Syntax

Here is a little tutorial on how the syntax works and some features

## Say Hello to the City of Stars

Simplest program for starters.

```lalalang
println("Hello City of Stars!!");
```

## Variables and Data Types

Currently the language supports integers, strings, and booleans, you can declare them like this. 

```lalalang
let director = "Damien Chazelle";
let great_movie = true;
let ibd_score = 8; # They know nothing >:(
```

You can only name variables with characters from the alphabet, so use *camelCase*.

## Operators

You have the classic arithmetic operators.

```lalalang
let lalalandDuration = 128;
let whiplashDuration = 107;

println(lalalandDuration + whiplashDuration);
println(lalalandDuration - whiplashDuration);
println(lalalandDuration * whiplashDuration);
println(lalalandDuration / whiplashDuration); 
```

The most simple relational ones.

```lalalang
let anotherDayOfSun = 7;
let someoneInTheCrowd = 8;
let cityOfStars = 10;
let aLovelyNight = 8;
let startAFire = 3;

println(aLovelyNight == someoneInTheCrowd);
println(startAFire != anotherDayOfSun);
println(cityOfStars > aLovelyNight);
println(startAFire < someoneInTheCrowd);
```

And the classic logical ones.

```lalalang
let shouldMiaGoToParis = false;
println(!shouldMiaGoToParis);

let shouldSebastianJoinTheBand = true;
let quitBeingAJazzPurist = true;
println(shouldSebastianJoinTheBand && shouldSebastianJoinTheBand);

let isMiaWithSebastian = false;
let isSebastianWithMia = false;
println(isMiaWithSebastian || isSebastianWithMia);
```

## Functions and Control Flow

Only conditionals exists for control flow.

```lalalang
let theSunIsNearlyGone = True;
let theLightsAreTurningOn = True;

if(theSunIsNearlyGone) {
    if(theLightsAreTurningOn) {
        println("What a waste of lovely night:(")
    }
}
```

Functions are first class citizens, so you declare a variable to a function.

```lalalang
let crowd = 4;
let isSomeOneInTheCrowd = fun(crowd) {
    if(crowd > 0) {
        println("There is someone in the crowd :D")
    } else {
        println("There is no one in the crowd D:")
    }
}
```

So use your creativity and make some recursive solutions.

```
let heat = 20;
let startAFire = fun(heat) {
    if(heat < 1700) {
        return heat * startAFire(heat + 2);
    }
    print("That is enough to start a fire!");
}
```

## Builtin Functions

There only exists two builtin functions:

* **println**: It prints whatever is passed to him with a break line at the end.
* **print**: Same as println but without the ending break line.
* **toString**: Convert an integers to an string in order to concatenate.

See the [example](../examples) section to check out how this is used.
