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
import sys, random, os
from psychopy import visual, core, event 
from datetime import datetime
# if you have issues installing psychopy, install the packages from dependencies.txt

###### ----------------- setting variables ------------------ ######

NUM_TRIALS = 6  # trial number in total - must be an even number for balanced randomization
trial_types = ["abdominal", "hands"] * (NUM_TRIALS // 2)
random.shuffle(trial_types)

random_break = random.randint(3, 9)  # Random break between 3 and 9 seconds

# background colors for each trial type and default color
trial_colors = {
    "hands": "green",
    "abdominal": "blue"
}

default_color = "grey"
#### ----------------- TEXT ------------------ ######

tutorial_texts = [
        "Velkommen til mave-spændings-eksperimentet. \n\nTryk på mellemrumstasten for at fortsætte.", 

        "I dette eksperiment vil du blive bedt om skiftevis at knytte dine hænder eller spænde i dine mavemuskler. "
        "Du vil blive bedt om at knytte dine hænder eller spænde dine mavemuskler i et minut.\n\n"
        "Hvis du ikke kan gøre det så længe, tryk på mellemrumstasten for at vise, at du er stoppet.\n\n"
        "Du vil derefter blive bedt om at svare på nogle spørgsmål om, hvordan det føltes. Tryk på mellemrumstasten for at fortsætte.",

        "Vi starter med en prøverunde. Følg instruktionerne på skærmen.\n\n"
        "Når skærmen er grøn, skal du knytte dine hænder.\n Når skærmen er blå, skal du spænde dine mavemuskler.\n\n" 
        "\nTryk på mellemrumstasten for at fortsætte."
    ]

break_text0 = "+" # intertrial stimulus 
break_text1 = "Prøverunden er nu slut. I eksperimentet skal du prøve at spænde dine mavemuskler eller knytte din hånd i et minut.\n\n" \
"Hvis du ikke kan gøre det så længe, så tryk på mellemrumstasten for at vise, at du er holdt op.\n\n" \
"Tryk på mellemrumstasten, når du er klar til at starte eksperimentet."
break_text2 = "Eksperimentet starter nu"
end_text = "Eksperimentet er nu slut.\n\nTak for din deltagelse!\n\nTryk på mellemrumstasten for at afslutte."


trial_templates = {
    "abdominal": {
        "anticipation": "Gør dig klar. Om lidt skal du spænde i dine mavemuskler.",
        "provocation": "Spænd i dine mavemuskler nu.\n\nHvis du ikke kan spænde mere, så tryk på mellemrumstasten.",
        "recovery": "Slap af i dine mavemuskler."
    },
    "hands": {
        "anticipation": "Gør dig klar. Om lidt skal du knytte dine hænder.",
        "provocation": "Knyt dine hænder nu.\n\nHvis du ikke kan knytte dine hænder længere, så tryk på mellemrumstasten.",
        "recovery": "Slap af i dine hænder."
    }
}

vas_questions_exp = {
    "abdominal": [
        {
            "question": "Blev du bange, da du spændte dine mavemuskler?",
            "labels": ["Slet ikke", "Meget bange"],
            "type": "fear"
        },
        {
            "question": "Gjorde det ondt, da du spændte dine mavemuskler?",
            "labels": ["Ingen smerte", "Værst tænkelige smerte"],
            "type": "pain"
        },
        {
            "question": "Havde du lyst til at undgå at spænde dine mavemuskler?",
            "labels": ["Slet ikke", "Rigtig meget"],
            "type": "avoidance"
        }
    ],
    "hands": [
        {
            "question": "Blev du bange, da du knyttede dine hænder?",
            "labels": ["Slet ikke", "Meget bange"],
            "type": "fear"
        },
        {
            "question": "Gjorde det ondt, da du knyttede dine hænder?",
            "labels": ["Ingen smerte", "Værst tænkelige smerte"],
            "type": "pain"
        },
        {
            "question": "Havde du lyst til at undgå at knytte dine hænder?",
            "labels": ["Slet ikke", "Rigtig meget"],
            "type": "avoidance"
        }
    ]
}

vas_questions_end = [
    {
        "question": "Oplevede du, at det at spænde i dine mavemuskler er ligesom når du har ondt i maven?",
        "labels": ["Slet ikke", "Rigtig meget"],
        "type": "similarity"
    },
    {
        "question": "Synes du opgaven var svær?",
        "labels": ["Ikke svær", "Meget svær"],
        "type": "difficulty"
    },
    {
        "question": "Synes du opgaven var ubehagelig?",
        "labels": ["Ikke ubehagelig", "Meget ubehagelig"],
        "type": "discomfort"
    }
]


## ------------------USER INPUT ------------------ ##

try:
    show_tutorial = int(input("Tutorial (1 = yes / 0 = no)?: "))
except ValueError:
    print("Invalid input. Please enter 1 or 0.")
    core.quit()


participant_ID = input("Participant ID:")

experiment_start = datetime.now()

experiment_data = []

###### ----------------- Create window and save keys ------------------ ######
# # Create a window
win = visual.Window(fullscr=True, color = default_color, units="pix")
#win = visual.Window(size=[800, 600], color="black", fullscr=True)

# Define keys
SPACE_KEY = 'space'
ESC_KEY = 'escape'

def check_for_quit(keys):
    if ESC_KEY in keys:
        win.close()
        core.quit()

################ DEFINTE TEXT FUNCTIONS ################

def show_text_screen(text, wait_time=None, allow_skip=False, background_color=None):
    if background_color:
        win.color = background_color
    else:
        win.color = default_color

    #try:
    message = visual.TextStim(win, text=text, color="white", height=30, wrapWidth=1000)
    message.draw()
    win.flip()

    timer = core.Clock()

    while True:
        keys = event.getKeys()
        check_for_quit(keys)

        if SPACE_KEY in keys and allow_skip:
            break
        if wait_time is not None and timer.getTime() > wait_time:
            break
   # finally:
    #    win.color = default_color # Always restore window color
    #    win.flip()


def show_text_with_countdown(text, countdown_seconds, allow_skip=False, background_color=None):
    if background_color:
        win.color = background_color
    else:
        win.color = default_color

    timer = core.Clock()

  #  try:
    while True:
        elapsed = timer.getTime()
        remaining = countdown_seconds - elapsed
        if remaining <= 0:
            break

        main_text = visual.TextStim(win, text=text, pos=(0, 100), color="white", height=30, wrapWidth=1000)
        timer_text = visual.TextStim(win, text=f"{int(remaining)} sekunder", pos=(0, -60), color="white", height=30) #-100 før

        main_text.draw()
        timer_text.draw()
        win.flip()

        keys = event.getKeys()
        check_for_quit(keys)

        if allow_skip and SPACE_KEY in keys:
            break

############### define visual analogue scale function ###############

def show_vas(question, labels):

    # show text
    vas_text = visual.TextStim(win, text=question, pos=(0, 200), color="white", height=30, wrapWidth=1000)

    # show slider
    slider = visual.Slider(win, ticks=(0,100), 
                           labels=labels, 
                           granularity=0, #continuous scale = VAS
                           size=(600, 50), #width, height of scale 
                           pos=(0, 0), # position on the screen - center 
                           labelHeight=25, # label text size
                           style='rating', # style of slider
                           color='white')

    # slider = visual.Slider(win, ticks=(0, 25, 50, 75, 100), labels=labels,
    #                        granularity=1, size=(800, 50), pos=(0, 0), style='rating', color='white')

    while True:
        vas_text.draw()
        slider.draw()
        win.flip()

        keys = event.getKeys()
        check_for_quit(keys)

        # Exit as soon as a rating is selected
        if slider.getRating() is not None and slider.rating is not None:
           # core.wait(0.5)  # Optional: brief pause for feedback
            return slider.getRating()


########### define tutorial function ###############

def run_tutorial(tut_text_list):
    for i, text in enumerate(tut_text_list):
        print(f"Tutorial screen {i+1} of {len(tut_text_list)}")  # Optional debug
        show_text_screen(text, allow_skip=True) 

    # run hands
    practice_phases = trial_templates["hands"]
    show_text_with_countdown(practice_phases["anticipation"], countdown_seconds=5, background_color='green')
    show_text_with_countdown(practice_phases["provocation"], countdown_seconds=30, allow_skip=True, background_color='green')
    show_text_screen(practice_phases["recovery"], wait_time=4)

    # # VAS questions
    for idx in vas_questions_exp["hands"]:
        rating = show_vas(idx["question"], idx["labels"])
        print(f"VAS Response [hands]: {idx['type']} = {rating}")


    show_text_screen(break_text0, wait_time= random_break) # intertrial interval

    # run abdominal
    practice_phases = trial_templates["abdominal"]
    show_text_with_countdown(practice_phases["anticipation"], countdown_seconds=5, background_color='blue')
    show_text_with_countdown(practice_phases["provocation"], countdown_seconds=30, allow_skip=True, background_color='blue')
    show_text_screen(practice_phases["recovery"], wait_time=4)

    # VAS questions
    for idx in vas_questions_exp["abdominal"]:
        rating = show_vas(idx["question"], idx["labels"])
        print(f"VAS Response [abdominal]: {idx['type']} = {rating}")

    # outro from tutorial text
    show_text_screen(break_text1, allow_skip=True) 


############### define experiment function ###############
def run_experiment():
    show_text_screen(break_text2, wait_time=3)

    for i, trial_type in enumerate(trial_types):
        print(f"Running Trial {i+1} — {trial_type.capitalize()}")

        # Get the current template
        phases = trial_templates[trial_type]

        # get color
        bg_color = trial_colors[trial_type]  # Get the trial-specific color


        # Show anticipation, provocation, recovery
        show_text_with_countdown(phases["anticipation"], countdown_seconds=5, background_color=bg_color)
        show_text_with_countdown(phases["provocation"], countdown_seconds=60, allow_skip=True, background_color=bg_color)
        show_text_screen(phases["recovery"], wait_time=3)

        # VAS questions
        vas_ratings = {}
        for idx in vas_questions_exp[trial_type]:
            rating = show_vas(idx["question"], idx["labels"])
            vas_ratings[idx["type"]] = rating
            print(f"VAS Response [{trial_type}]: {idx['type']} = {rating}")
   
         # Prepare trial data dictionary
        trial_data = {
            "participant_ID": participant_ID,
            "trial_number": i + 1,
            "trial_type": trial_type
           # "tensing_duration": tensing_duration,
            #"trial_start": provocation_start.strftime("%Y-%m-%d %H:%M:%S"),
            #"trial_end": provocation_end.strftime("%Y-%m-%d %H:%M:%S"),
           # "experiment_start": experiment_start.strftime("%Y-%m-%d %H:%M:%S"),
            #"experiment_date": experiment_start.strftime("%Y-%m-%d")
        }

        # Add VAS ratings to trial data
        trial_data.update(vas_ratings)

        experiment_data.append(trial_data)


        show_text_screen(break_text0, wait_time=random_break)  # ITI

        # Optionally store ratings per trial
        # e.g., append to a list of dicts


########## SAVE DATA FUNCTION ##########

def save_data(vas_ratings_end):
   # filename = f"provocation_task_{participant_ID}.csv"
    # Append the end-of-experiment VAS questions as a summary row
    end_row = {
        "participant_ID": participant_ID,
        "trial_number": "end",
        "trial_type": "end_questions"
    }
    end_row.update(vas_ratings_end)
    experiment_data.append(end_row)

    df = pd.DataFrame(experiment_data)

    # Add metadata columns
    df["experiment_date"] = experiment_start.strftime("%Y-%m-%d")
    df["experiment_start_time"] = experiment_start.strftime("%H:%M:%S")
    df["experiment_end_time"] = experiment_end.strftime("%H:%M:%S")

    # Ensure 'data' directory exists
    data_folder = "data"
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)

    filename = f"provocation_participant_{participant_ID}_{experiment_start.strftime('%Y%m%d_%H%M%S')}.csv"
    filepath = os.path.join(data_folder, filename)
    df.to_csv(filepath, index=False)
   # df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")

# --------- MAIN PROGRAM ----------

if show_tutorial == 1:
    run_tutorial(tutorial_texts)

# run experiment
run_experiment()

# end of experiment questions
vas_ratings_end = {}
for idx in vas_questions_end:
    rating = show_vas(idx["question"], idx["labels"])
    vas_ratings_end[idx["type"]] = rating
    print(f"VAS Response: {idx['type']} = {rating}")


# End screen
show_text_screen(end_text, allow_skip=True)
experiment_end = datetime.now()

# save data from experiment
save_data(vas_ratings_end)

win.close()
core.quit()

