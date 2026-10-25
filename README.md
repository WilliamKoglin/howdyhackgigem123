### NetWorking

First-person beach volleyball with no controller, no install. Just a webcam and a browser.

Beach Howdyball is a browser-based, first-person beach volleyball game controlled through real-time webcam hand tracking. Raise, lower, and position your hands to dig, set, and spike your way through a rally. If the camera isn't cooperating, a mouse-driven fallback keeps you playing.

# Features
Gesture-based controls - Your hands are the controller.

Three core volleyball actions - Dig (both hands low), Set (both hands high), and Spike (either hand high).

Timing window mechanic - Time your swings for when the ring closes to succeed.

Input mode optionality - Webcam hands or mouse hands are options for people to play. If one stops working, users have the ability to switch on the fly.

Full match loop and replayability - Matches last up to 15 points, and when a game is over players have a smooth transition to play again.

Zero install/account - Runs simply and concisely in your browser.


# Controls:
Action              Input
Aim                 Hands(camera) / mouse
Swing               Click/space
One-handed hit      One hand up (camera) / shift
Switch mode         M
Restart             R

# Get Started
1. Open the game in a modern desktop browser (Chrome/Edge recommended for camera + WebGL support)
2. Allow Camera Access
3. Select preferred controls and click "Lets Play"
4. Dig, set and spike. First to 15 wins.

No bulky installs, no account setup, just easy access fun.

## How it works
This single-file webapp composes three subsystems:

# Perception
The camera pulls frames from getUserMedia, feeds them to a hand-landmark model, and reduces the landmark set into a small, relevant vector. 

Then, the position is inferred to attmpt to recognize three discriminable states:
both hands LOW
both hand HIGH
one hand HIGH

These three states require both hands visible to determine a two-handed set from a one-handed spike. Reducing the problem of reading a body to height and count keeps per-frame inference cheap enough to stay inside render budget.

There is an alternative for serving but that just checks if either hand or both are in the correct positions.

# The timing window
While the instructions tell the user what to do and when to do it explicitly, some instructions can be ambiguous. We used a closing ring mechanic similar to rhythm games to choose a familiar timing mechanic.

The contact inputs must land when the ring closes. The Open Time begins slightly before the ring closes, giving players grace for imperfect timing, while perfect inputs are rewarded and displayed on screen. Although the window of contact opens slightly early, the wrong number of hands (ie trying to set a spike) will penalize the player. The Close Time occurs when the ring collapses.

# Game simulation
The rally is a scripted state machine around the loop P1 (dig) digs, P2 (set) sets, P1 spikes. The state lives in a few variables:
gameState - idle, startingCamera, reading, playing, matchOver
score - {us:them}, match ends at 15
rallyPhaase - which contact is currently expected between dig, set, and spike
ball - position and velocity, affected by simple physics (gravity and impules applied by contact)

Successful contact applies an impulse whose direction and strength is scaled by hit quality. Mistimed swings or wrong gestures breaks the rally and awards a point. matchOver beings up the "Match Over, Play Again" UI and resets the state of gameplay.

## Rendering
A first-person camera renders the beach court and ball. The on-screen HUD elements gives the user information on the current score and what action they should be taking, or if the ball is on the CPU's side of the court.

The prompt, ball, and timing ring gives the user constant feedback on what to do.

## Input abstraction
Both webcam hands and mouse hads feed the same intent (height and count) because the game consumes abstracted intent. Switching modes with M is then seamless and the mouse path is just as functional and more input styles are open ended to implementation.

Mouse inputs are important to have as hand tracking can degrade in poor lighting and tight spaces, so the more traditional inputs are a fallback feature that preserves quality.

### Constraints
Single-file deployment - the file ships itself as a HTML file and is trivial to host statically
Browser requirements - needs getUserMedia (camera) permission and WebGL support. Chromium recomended
Lighting sensitive - hand tracking quality depends on even lighting and both hands being in frame. Mouse hands are a safe fallback
Stateless - no accounts, backend, or persistence. Sessions end at 15 points

### Difficulties and solutions
Throughout development, we ran into a few problems which are listed below along with the solutions we came up with.

Problem 1: UI
During development we explored different options including leaning, hand signs, and full body movements to explore what would be suitable for precise and interactive input. We settled on a take that had generous hand area that displayed where the computer read your hands at live for constant visual feedback of what the program was reading.

Problem 2: Point of view
We also experimented with camera switches between different players and both sides of the net. Constant point of view switches can be disorienting without the right support. We chose to use two points of view in the first person, which links with out input style and UI to give the user feedback on where they are on the court.
We changed viewpoints to the other side of the court to allow user's rest time and prepare them for the next set of actions.

Problem 3: Variance
Having balls appear out of reach or in the same spot evey time isn't fun. We chose to make variance in CPU serves to increase difficulty and have player actions be generally on the same level (low/high) for specific actions (dig set spike).

Problem 4: Suggestions and instructions
We employed a variety of output to give the user feedback since good games have good instructions. Users are explicitly given instructions at the start and in the top-right corner live, but information is also conveyed implicitly via ball position, the timing ring, audio feedback, and the score.
