# FriendshipModel
This is a friendship model project for the game theory class

Proposed tasks:

## Step 1:
- 20*20 grid, 25% population (100 agents)
- strategies of each agent: social/non-social
- Utility function = (1-s)*Pi + s*Pj (i - agent itself, j - the other agent that this agent is interacting with, s - social preference, Pi - payoff function of i, Pj - payoff j gets by interacting with i)

## Step 2:
- randomly die out 5% population (5 agents)
- refill 5 new agents who are the offsprings of the agents with the highest utility function values in the previous round
- the social preference of the offspring has 5% probability to mutate

## step 3:
- the big model captures the statistic of the collaborative agents
- run the model
- visualization of the model
