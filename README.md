# resistanceAI
AI platform for the card game resistance.

# Description
1. Three agents implemented: Greedy_agent.py, li_agent(model based agent), mct_agent(Monte Carlo Tree search agent)

2. game.py has been edited to always make first two agents as spy for testing, changed code in line 28 and 32, commenting out the suffle. 

3. random_agent has been changed, introducing the seed value seed = 1 in the def __init__() of random_agent.py

4. Everything keeps the format of benchmarking before the submitting. 

5. test_vsall.py is testing entry point, refers to the comment in the file.

6. train_mct.py is pre-learning entry point, the agents have already been trained with ramdon agents for 80000 rounds of game (random agents are strictly spies), refering to the comment in the file.

7. mctnodes_dict.json is the trained dictionary for mct agent to look up.

# Getting started
--python3 test_vsall.py
--python3 train_mct.py


