##### Abdominal Tensing Task #####
# This script is used to run the abdominal tensing task experiment
# Created by: Sigrid Bom
# Date: 2025-04-01

# comments
#-
#-
#-

#------------------------- PACKAGES -------------------------#

# importing packages
import pandas as pd
import sys, random 
from psychopy import visual, core, event 
# if you have issues installing psychopy, install the packages from dependencies.txt

###### ----------------- setting variables ------------------ ######

NUM_TRIALS = 6  # Must be an even number for balanced randomization
trial_types = ["abdominal", "hands"] * (NUM_TRIALS // 2)
random.shuffle(trial_types)

random_break = random.randint(3, 9)  # Random break between 3 and 9 seconds

#### ----------------- TEXT ------------------ ######

tutorial_texts = [
        "Velkommen til mave-spændings-eksperimentet. \nTryk på mellemrumstasten for at fortsætte.", 
        "I dette eksperiment vil du blive bedt om skiftevis at spænde i dine mavemuskler og knytte dine hænder.\n"
        "Du vil blive bedt om at knytte dine hænder eller spænde dine mavemuskler i et minut ad gangen.\n"
        "Hvis du ikke kan gøre det så længe, tryk på mellemrumstasten for at vise, at du er stoppet.\n"
        "Du vil derefter blive bedt om at svare på nogle spørgsmål om, hvordan det føltes. Tryk på mellemrumstasten for at fortsætte.",
        "Vi starter med en prøverunde. Følg instruktionerne på skærmen.\nTryk på mellemrumstasten for at fortsætte."
    ]

break_text0 = "+" # intertrial stimulus 
break_text1 = "Prøverunden er nu slut. I eksperimentet skal du prøve at spænde dine mavemuskler eller knytte din hånd i et minut.\n" \
"Hvis du ikke kan gøre det så længe, så tryk på mellemrumstasten for at vise, at du er holdt op.\n" \
"Tryk på mellemrumstasten, når du er klar til at starte eksperimentet."
break_text2 = "Eksperimentet starter nu"


trial_templates = {
    "abdominal": {
        "anticipation": "Gør dig klar. Om lidt skal du spænde i dine mavemuskler.",
        "provocation": "Spænd i dine mavemuskler nu.",
        "recovery": "Slap af i dine mavemuskler."
    },
    "hands": {
        "anticipation": "Gør dig klar. Om lidt skal du knytte dine hænder.",
        "provocation": "Knyt dine hænder nu.",
        "recovery": "Slap af i dine hænder."
    }
}

vas_questions = [
    "Hvor intenst var ubehaget?",
    "Hvor ubehageligt føltes det?",
    "Hvor meget spændte du?"
]

# trial_texts = [
#         "VENT\n Om lidt skal du spænde i dine mavemuskler.",
#         "Spænd i dine mavemuskler.", # add timer 
#         "Slap af i maven. Forsøget fortsætter om lidt.", # 2
#         "VENT\n Om lidt skal du spænde i dine mavemuskler.",
#         "Spænd i dine mavemuskler.", # add timer 
#         "Slap af i maven. Forsøget fortsætter om lidt.", # 5
#         "VENT\n Om lidt skal du spænde i dine mavemuskler.",
#         "Spænd i dine mavemuskler.", # add timer 
#         "Slap af i maven. Forsøget fortsætter om lidt." # 8, 11, 14
#     ]

## ------------------USER INPUT ------------------ ##

try:
    show_tutorial = int(input("Tutorial (1 = yes / 0 = no)?: "))
except ValueError:
    print("Invalid input. Please enter 1 or 0.")
    core.quit()


#user_input_ID =input("Participant ID:")
#show_tutorial = int(input("Tutorial (1 = yes /0 = no)?:"))
#participant_ID = input("Participant ID:")


###### ----------------- EXPERIMENT CODE ------------------ ######
# # Create a window
win = visual.Window(fullscr=True, color = "grey", units="pix")
#win = visual.Window(size=[800, 600], color="black", fullscr=True)

######## CHAT's CODE ##########


################ DEFINTE TEXT FUNCTIONS ################
# Define keys
SPACE_KEY = 'space'
ESC_KEY = 'escape'

def check_for_quit(keys):
    if ESC_KEY in keys:
        win.close()
        core.quit()

def show_text_screen(text, wait_time=None, allow_skip=False):
    message = visual.TextStim(win, text=text, color="white", height=30, wrapWidth=1000)
    message.draw()
    win.flip()  # << You MUST call this to show the drawn stimuli!

    timer = core.Clock()
    while True:
        keys = event.getKeys()
        check_for_quit(keys)

        if SPACE_KEY in keys and allow_skip:
            break
        if wait_time is not None and timer.getTime() > wait_time:
            break

def show_text_with_countdown(text, countdown_seconds, allow_skip = False):
    timer = core.Clock()
    
    while True:
        elapsed = timer.getTime()
        remaining = countdown_seconds - elapsed
        if remaining <= 0:
            break

        # Prepare stimuli
        main_text = visual.TextStim(win, text=text, pos=(0, 100), color="white", height=30, wrapWidth=1000)
        timer_text = visual.TextStim(win, text=f"{int(remaining)} sekunder", pos=(0, -100), color="white", height=40)
        
        # Draw and flip
        main_text.draw()
        timer_text.draw()
        win.flip()

        # Check for quit
        keys = event.getKeys()
        check_for_quit(keys)

        if allow_skip and "space" in keys:
            break


def show_vas(question):
    vas_text = visual.TextStim(win, text=question, pos=(0, 200), color="white", height=25)
    slider = visual.Slider(win, ticks=(0, 25, 50, 75, 100), labels=["Not at all", "", "", "", "Very much"],
                           granularity=1, size=(800, 50), pos=(0, 0), style='rating', color='white')

    while True:
        vas_text.draw()
        slider.draw()
        win.flip()

        keys = event.getKeys()
        check_for_quit(keys)

        # Exit as soon as a rating is selected
        if slider.getRating() is not None and slider.rating is not None:
            core.wait(0.5)  # Optional: brief pause for feedback
            return slider.getRating()

########### define tutorial function ###############

def run_tutorial(tut_text_list):
    for i, text in enumerate(tut_text_list):
        print(f"Tutorial screen {i+1} of {len(tut_text_list)}")  # Optional debug
        show_text_screen(text, allow_skip=True) 

    # run hands
    practice_phases = trial_templates["hands"]
    show_text_with_countdown(practice_phases["anticipation"], countdown_seconds=5)
    show_text_with_countdown(practice_phases["provocation"], countdown_seconds=30, allow_skip=True)
    show_text_screen(practice_phases["recovery"], wait_time=4)

    for question in vas_questions:
        show_vas(question)

    show_text_screen(break_text0, wait_time= random_break) # intertrial interval

    # run abdominal
    practice_phases = trial_templates["abdominal"]
    show_text_with_countdown(practice_phases["anticipation"], countdown_seconds=5)
    show_text_with_countdown(practice_phases["provocation"], countdown_seconds=30, allow_skip=True)
    show_text_screen(practice_phases["recovery"], wait_time=4)

    for question in vas_questions:
        show_vas(question)

    # outro from tutorial text
    show_text_screen(break_text1, allow_skip=True) 


############### define experiment function ###############
def run_trials():
    show_text_screen(break_text2, wait_time=3)

    for i, trial_type in enumerate(trial_types):
        print(f"Running Trial {i+1} — {trial_type.capitalize()}")

        # Get the current template
        phases = trial_templates[trial_type]

        # Show anticipation, provocation, recovery
        show_text_with_countdown(phases["anticipation"], countdown_seconds=5)
        show_text_with_countdown(phases["provocation"], countdown_seconds=60, allow_skip=True)
        show_text_screen(phases["recovery"], wait_time=3)

        # VAS questions
        ratings = {}
        for question in vas_questions:
            rating = show_vas(question)
            ratings[question] = rating
            print(f"VAS Response: {question} = {rating}")

        show_text_screen(break_text0, wait_time=random_break)  # ITI

        # Optionally store ratings per trial
        # e.g., append to a list of dicts


# def run_experiment(exp_text_list):
#   #  for text in exp_text_list:
#   #  show_text_screen(text)

#     for i, trial in enumerate(exp_text_list):
#         show_text_screen(trial, wait_time=5)  # Shows for 5 sec or until space is pressed
        
#         if i in [2,4,6,8,10]:#== 2 |  == 0:#== 2:
#             rating = show_vas("Indsæt spørgsmål her?")
#             print(f"Rating: {rating}")  # You might store this instead

# --------- MAIN PROGRAM ----------

# Run blocks
# if show_tutorial == 1:
#     run_tutorial(tutorial_texts)
# run_experiment(trial_texts)

if show_tutorial == 1:
    run_tutorial(tutorial_texts)

# run experiment
run_trials()

# End screen
show_text_screen("Thank you for participating!\n\nPress space to exit.", allow_skip=True)
win.close()
core.quit()




########## own code below##########
# ## --------------- TEXT ------------------- ##

# intro1 = "Velkommen til mave-spændings-eksperimentet. \nTryk på mellemrumstasten for at fortsætte."
# intro2 = "test test test "





# ## ---------------- TUTORIAL ------------------ ##
# if user_input_tutorial == "1":
#     # Define text stimuli
#     instruction_text = visual.TextStim(win, text=intro1, color="white")
#     # question_text = visual.TextStim(win, text="How happy do you feel?", pos=(0, 0.2), color="white")
#     instruction_text.draw()
#     win.flip()
#     event.waitKeys(keyList=["space"])
# else:
#     pass


# ## ----------------- EXPERIMENT ------------------ ##

# instruction_text = visual.TextStim(win, text=intro2, color="white")
# instruction_text.draw()
# win.flip()
# event.waitKeys(keyList=["space"])
# # Define text stimuli
# #instruction_text = visual.TextStim(win, text=intro1, color="white")
# # question_text = visual.TextStim(win, text="How happy do you feel?", pos=(0, 0.2), color="white")

# # # Define a visual analogue scale (VAS)
# # rating_scale = visual.Slider(win, 
# #                              ticks=[0, 25, 50, 75, 100], 
# #                              labels=["0", "25", "50", "75", "100"],
# #                              granularity=1, 
# #                              style=['rating'], 
# #                              color='red')

# # Show instruction screen
# instruction_text.draw()
# win.flip()
# event.waitKeys(keyList=["space"])

# # # Show question screen
# # while rating_scale.noResponse:  # Wait for response
# #     win.flip()
# #     question_text.draw()
# #     rating_scale.draw()

# # # Save the response
# # response = rating_scale.getRating()
# # print(f"Participant's rating: {response}")

# # End experiment
# win.close()
# core.quit()