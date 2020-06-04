
import json

def create_card(banks_list):
    # Initialize Card schema
    card = {
        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
        "type": "AdaptiveCard",
        "version": "1.2",
        "body": [
            {
                "type": "Container",
                "items": []
            }
        ]
    }
    
    card_items = card['body'][0]['items']
    
    # Add items
    for (i, bank) in enumerate(banks_list):
        all_elements = []
        # Header + Separator
        header = {
            "type": "TextBlock",
            "text": f"Nearby {i}",
            "spacing": "large",
            "separator": "True"
        }
        # Initialize the columns set
        column_set = {
            "type": "ColumnSet",
            "columns": []
        }
        
        # Now for 2-width column
        for _ in range(1):
            column_width_2 = {
                "type": "Column",
                "width": 2,
                "items": []
            }
            # Add elements to 2-width column
            for _ in range(1): 
                # Add title to the 2-width column
                column_width_2['items'].append({
                    "type": "TextBlock",
                    "text": "BANK OF LINGFIELD BRANCH"
                })
                # Add name of the branch in bold
                column_width_2['items'].append({
                    "type": "TextBlock",
                    "text": f"{bank.name}",
                    "weight": "Bolder",
                    "size": "ExtraLarge",
                    "spacing": "None"
                })
                # Add rating
                column_width_2['items'].append({
                    "type": "TextBlock",
                    "text": "4.2 Stars",
                    "isSubtle": "True",
                    "spacing": "None"
                })
                # Add review
                column_width_2['items'].append({
                    "type": "TextBlock",
                    "text": "**Matt H. said** Im compelled to give this place 5 stars due to the number of times Ive chosen to bank here this past year!",
                    "size": "Small",
                    "wrap": "True"
                })
                
        # Now for the 1-width column
        for _ in range(1):
            column_width_1 = {
                "type": "Column",
                "width": 1,
                "items": []
            }
            # Add image to the column
            for _ in range(1):
                column_width_1['items'].append({
                    "type": "Image",
                    "url": "https://www.financialtechnologyafrica.com/wp-content/uploads/2019/06/building-with-bank-on-front.jpg",
                    "size": "auto",
                    "altText": "Seated guest drinking a cup of coffee"
                    })
                
        # Add 2-width and 1-width columns to the column set (2 -> 1)
        column_set['columns'].append(column_width_2)
        column_set['columns'].append(column_width_1)
        
        # Add header and column set to all container
        all_elements.append(header)
        all_elements.append(column_set)
        
        #################################################################
        # Now for actions
        action_set = {
            "type": "ActionSet",
            "actions": []
        }
        
        # Add show me on a map button to actions set
        show_me_on_map_button = {
            "type": "Action.OpenUrl",
            "title": "Show me on a map!",
            "url": "https://adaptivecards.io"
        }
        
        # action set has an expandible "show card"
        showcard = {
            "type": "Action.ShowCard",
            "title": "Show Available Appointments",
            "card": {
                "type": "AdaptiveCard",
                "body": []
            }
        }

        # add actions to the show card's body - one per appointment
        showcard_body = showcard['card']['body']
        
        for (j, appointment) in enumerate(bank.appointments):
            showcard_column_set = {
                "type": "ColumnSet",
                "style": "emphasis",
                "columns": []
            }
            
            showcard_column_set_columns = showcard_column_set['columns']
            # Add Appointment margin
            showcard_column_set_columns.append({
                "type": "Column",
                "style": "emphasis",
                "items": [
                    {
                        "type": "TextBlock",
                        "text": f"Appointment Slot {j}"
                    }
                ],
                "bleed": "true",
                "width": "stretch"
            })
            
            # Add start time label
            showcard_column_set_columns.append({
                "type": "Column",
                "style": "emphasis",
                "items": [
                    {
                        "type": "TextBlock",
                        "text": f"Start Time: {appointment.start_time}"
                    }
                ],
                "width": "stretch"
            })
            
            # Add end time label
            showcard_column_set_columns.append({
                "type": "Column",
                "style": "emphasis",
                "items": [
                    {
                        "type": "TextBlock",
                        "text": f"End Time: {appointment.end_time}"
                    }
                ],
                "width": "stretch"
            })
            
            # Add appointment booking button
            showcard_column_set_columns.append({
                "type": "Column",
                "width": "stretch",
                "items": [
                    {
                        "type": "ActionSet",
                        "actions": [
                            {
                                "type": "Action.Submit",
                                "title": "Book this appointment!"
                            }
                        ]
                    }
                ]
            })
            
            # Add column set to showcard body
            showcard_body.append(showcard_column_set)
            
        # Add the above actions to the action set
        action_set['actions'].append(showcard)
        action_set['actions'].append(show_me_on_map_button)
        
        # Add to all elements
        all_elements.append(action_set)
        card_items.extend(all_elements)
        
    return card
