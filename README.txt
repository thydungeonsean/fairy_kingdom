Fairy Kingdom
a game for Pyweek 24

Coding and art by Sean Marzec.

The hapless mushlocks are the rulers of the underworld. But it is you,
the fairies, who are behind their success. Use your powers to help the
mushroom people thrive.

----------------------------------------------------------------------------------
CONTROLS
--------
Press space to skip a turn.

W, A, S, D to scroll the view area.

In the actual game, press x to take a screen shot. (It's not very robust, it will 
save over previous screen shots if you start a new session and take more. If you
want to keep them move them out of the directory when you're done.)

In the actual game, press / to toggle fullscreen or windowed. 
- (I didn't have time to make anything smart about resolutions and scales.
If you run from source update src.constants.py to adjust scaling and 
screen size. No promises things will work though.)

Other than than, it is mostly mouse controlled, and hopefully intuitive.

----------------------------------------------------------------------------------
GAME
-----

This is a turn based game. Each time you use a power a turn will trigger,
and all ai objects on the map will take a few actions.

Mushlocks gather food, collect gems, and sleep, but mostly wander aimlessly.
If two mushlocks sleep adjacent to one another, they morph into a new house.
If a mushlock starves he will eventually become a dead stump.

Rivers generate green growth which in turn generates the food mushlocks need to
thrive. The map is procedurally generated each run, and is not guarenteed to be 
interconnected. But you can find picks and mine most wall and rock tiles, so
it's no big deal. Be careful though, there could be something lurking in those
sealed off vaults!

There is no "winning" in fairy kingdom. Just play until you are bored. Or
wiped out by the orcish hordes. You will get a score!

No save game system implemented at this time.

----------------------------------------------------------------------------------
POWERS
------
Fairy Powers:
Lure - place a shiny thing that mushlocks love to check out.
See - reveal an area of the shrouded caverns - also see the gems hidden in the walls.
Sleep - put a silly mushlock to sleep!
Gust - click adjacent to mushlocks to shove them around the map.
River - summon a mighty river spirit to bring life to the underworld! Rivers are
placed on walls with floor below them.
Rock - smash stuff with a rock. Try it out!
Mark - x marks the spot! put down a magic x that mining mushlocks enjoy striking.

----------------------------------------------------------------------------------
HINTS
------
- keep an eye out for when a mushroom stops next to a sleeping mushroom. You can
cast sleep on him to form a house.
- summon rivers to create good food sources, but be careful not to mash your houses
with the deluge! (unless you want to do that.)
- the more food mushlocks bring back to the house, the faster it will spawn new
mushlocks.
- form a house right in a big patch of vegetation to jump start a colony

----------------------------------------------------------------------------------
TO RUN
-------
A stand alone .exe is included to run the game. Run fairy_kingdom.exe.

The source is also included. The game is written in python 2.7. You will need
pygame as well. run python fairy_kingdom.py from the main directory.
---------------------------------------------------------------------------------

Thank you for reading! I hope you enjoy. I really enjoyed making it.
----------------------------------------------------------------------------------
Fairy Kingdom was created in one week for Pyweek #24. Pyweek was really fun.

----------------------------------------------------------------------------------

Copyright (c) Sean Marzec, 2017.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

    (1) Redistributions of source code must retain the above copyright
    notice, this list of conditions and the following disclaimer. 

    (2) Redistributions in binary form must reproduce the above copyright
    notice, this list of conditions and the following disclaimer in
    the documentation and/or other materials provided with the
    distribution.  
    
    (3)The name of the author may not be used to
    endorse or promote products derived from this software without
    specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT,
INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.