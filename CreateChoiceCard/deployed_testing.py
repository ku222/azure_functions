
#%%

import requests
import json


#%% Example payload in dict form
# u'\u2588'


prompts = ['How many languages do you speak', 'What is your name']
actions = ['languages', 'names']

def create_card(prompts, actions):
    blue_background = "https://digitalsynopsis.com/wp-content/uploads/2017/02/beautiful-color-gradients-backgrounds-047-fly-high.png"
    white_background = "https://i.pinimg.com/originals/f5/05/24/f50524ee5f161f437400aaf215c9e12f.jpg"
    card = AdaptiveCard(backgroundImage=blue_background)
    for (prompt, action) in zip(prompts, actions):
        card.add([
            "items",
            ActionSet(),
                "action",
                ActionSubmit(title=prompt, data={"action": action}),
        "^"
        ])
    
    return card.to_json()
        
create_card(prompts, actions)
