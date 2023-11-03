# RoughClimate
Simulator game of cities suffering through increasingly rough weather conditions, originally meant

## Play
The code is playable [here](https://trinket.io/pygame/8b19108203).

However, you can run it on your machine if you want, see requirements below.

## Requirements
- PyGame
- Python 3.11 or higher

## To Do list
Key:
- ⬜ (Must Have) Means it is required for basic MVP
- ⚪ (Should Have) Means that it would be very nice to have
- 🤍 (Could Have) Means it is someting that might be cool but not needed
- 🟩 Done
- 🟨 Kinda done/In progress
- 🟥 Not started
### Interface
🟩 show cities distinct by country  
🔴 show features such as defences, population, infrastructure  
🟩 display cities on the map (cirular positioning)  
🧡 in random positions with borders  
🔴 display movement of resources  
🔴 display disasters  
🔴 start and end menu  

### Functionality
🟩 connect cities  
🟩 generate initial city resources and pops  
🟩 look at how everything can be accessed from logic  
🟩 resource consumption
- 🟩 food every day
- 🟩 building once a day

### Testing and QA
🟥 play the for testing (with help Andras and Louis Glantfield hopefully)
- test it displays and works as it should 🟥
- test difficulty 🟥
- test functionality (stuff you should be able to do and you should not) 🟥
- test for values (for example is 500 cap for building infrastructure too little, initial values, luck scaling, etc.) 🟥  

🔴 make the comments better, @params and such  
🔴 refactor code, especially the send and receive functions  

### Brainstorm corner
🟨 investing resources -> limited to 1 per day (Should I?????)
- 1 def from 10 iron 🟩
- 1 infrastructure from 1 wood 🟩

🟩 sending resources  
🟨 think about the rest  
🟨 Options for actions can be 
- invest resources 🟩
- send resources 🟩
- trading resources??? 🧡
    - ask for resources 🧡
    - respond to an ask for resources? 🧡