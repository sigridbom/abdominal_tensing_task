##### Abdominal Tensing Task #####
# This script is used to run the abdominal tensing task experiment
# Created by: Sigrid Bom Nielsen, PhD-student at Aarhus University, Denmark
# Date: 2025-04-01

# comments / last changes:
#-
#-
#-

#------------------------- PACKAGES -------------------------#

# importing packages
import sys, random, os
from datetime import datetime
import pandas as pd
import pygame
from psychopy import visual, core, event, sound
# if you have issues installing psychopy, install the packages from dependencies.txt


###### ----------------- setting variables ------------------ ######

trials_number = 8  # trial number in total - must be an even number for balanced randomization
exp_provoke_duration = 60  # maximum duration for the provocation phase in the experiment in seconds
tutorial_provoke_duration = 30  # duration for the provocation phase in the tutorial in seconds
tutorial_trial_types = ["hands", "abdominal"]  # for the tutorial, we only use one of each type and we start with hands


# background colors for each trial type and default color
trial_colors = {
    "hands": "green",
    "abdominal": "blue"
}
default_color = "grey"

save_tutorial_data = True  # Set to True if you want to save tutorial data, False otherwise

# Define keys
SPACE_KEY = 'space'
ESC_KEY = 'escape'

####------------------ setting paths/variables you shouldn't change ------------------####

pygame.mixer.init()
beep_tone = pygame.mixer.Sound("stimuli/short_beep.wav")

random_break = random.randint(3, 9)  # Random break between 3 and 9 seconds - intertrial interval

##### ----------------- generate random trial sequence------------------ ######

def generate_trials(num_trials):
    assert num_trials % 2 == 0, "Number of trials must be even."

    # Initial balanced list
    trial_types = ["abdominal", "hands"] * (num_trials // 2)

    valid = False
    while not valid:
        random.shuffle(trial_types)
        valid = True
        for i in range(2, num_trials):
            if trial_types[i] == trial_types[i-1] == trial_types[i-2]:
                valid = False
                break

    return trial_types

trial_types = generate_trials(trials_number)

#### ----------------- TEXT ------------------ ######

tutorial_texts = [
        "Velkommen til mave-spændings-eksperimentet. \n\nTryk på mellemrumstasten for at fortsætte.", # screen 1 

        "I dette eksperiment skal du skiftevis knytte dine hænder eller spænde i dine mavemuskler. ", # screen 2
        
        "Du skal knytte dine hænder eller spænde dine mavemuskler i et minut ad gangen.\n\n"
        "Hvis du ikke kan gøre det så længe, tryk på mellemrumstasten for at vise, at du er stoppet.\n\n"
        "Husk at trække vejret normalt.\n\n"
        "Du bedes derefter svare på nogle spørgsmål om, hvordan det føltes. Tryk på mellemrumstasten for at fortsætte.", # screen 3

        "Når skærmen er grøn, skal du knytte dine hænder.\n\nNår skærmen er blå, skal du spænde dine mavemuskler.\n\n" # screen 4
        "Det står altid på skærmen, hvad du skal gøre.\n\n"
        "Når du skal knytte dine hænder eller spænde dine mavemuskler, vil du høre en kort bip tone. Du hører lyden igen, når der er gået et minut, eller hvis du stopper før tid.\n\n",
        
        "Vi starter med en prøverunde.\n\n" # screen 5
        "I prøverunden skal du kun knytte dine hænder eller spænde dine mavemuskler i 30 sekunder.\n\n"
        "Hvis du har nogen spørgsmål, kan du stille dem til forsøgslederen nu.\n\n"
        "Tryk på mellemrumstasten for at starte prøverunden."
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
        "question": "Synes du opgaven var svær?",
        "labels": ["Ikke svær", "Meget svær"],
        "type": "difficulty"
    },
    {
        "question": "Synes du opgaven var ubehagelig?",
        "labels": ["Ikke ubehagelig", "Meget ubehagelig"],
        "type": "discomfort"
    },
    {
        "question": "Oplevede du, at det at knytte dine hænder er ligesom, når du har ondt i maven?",
        "labels": ["Slet ikke", "Rigtig meget"],
        "type": "similarity_hands"
    },
    {
        "question": "Oplevede du, at det at spænde i dine mavemuskler er ligesom, når du har ondt i maven?",
        "labels": ["Slet ikke", "Rigtig meget"],
        "type": "similarity_abdominal"
    }
]


## ------------------USER INPUT ------------------ ##

def get_yes_no_input(prompt):
    while True:
        user_input = input(prompt).strip()
        if user_input in ('0', '1'):
            return int(user_input)
        print("Invalid input. Please enter 1 (yes) or 0 (no).")

show_tutorial = get_yes_no_input("Tutorial (1 = yes / 0 = no)?: ")
#participant_ID = input("Participant ID:").strip()

while True:
    participant_ID = input("Participant ID:").strip()
    if " " in participant_ID:
        print("Invalid ID: spaces are not allowed. Please try again.")
    elif participant_ID == "":
        print("Invalid ID: input cannot be empty. Please try again.")
    else:
        break


###### ----------------- Create window and define quit with esc ------------------ ######


# # Create a window
win = visual.Window(fullscr=True, color = default_color, units="pix")

# always close the window and quit the experiment on ESC key
def check_for_quit(keys):
    if ESC_KEY in keys:
        win.close()
        core.quit()

################ DEFINTE TEXT FUNCTIONS ################

# def show_text_screen(text, wait_time=None, allow_skip=False, background_color=None, centered=True):
#     if background_color:
#         win.color = background_color
#     else:
#         win.color = default_color

#     # Set text alignment and position
#     if centered:
#         align = 'center'
#       #  pos = (0, 0)
#     else:
#         align = 'left'
#         #pos = (-0.8, 0.4)  # Adjust position based on your screen units

#     message = visual.TextStim(
#         win,
#         text=text,
#         color='white',
#         height=30,         # Use relative height like 0.05 if using 'height' units
#         wrapWidth=1000,       # Adjust for line wrapping
#        # pos=(0,0),
#         alignText=align#,     # Newer PsychoPy uses alignText for alignment
#         #units='height'       # Optional: can be 'norm', 'pix', etc.
#     )

#     message.draw()
#     win.flip()

#     timer = core.Clock()

#     while True:
#         keys = event.getKeys()
#         check_for_quit(keys)

#         if SPACE_KEY in keys and allow_skip:
#             break
#         if wait_time is not None and timer.getTime() > wait_time:
#             break


def show_text_screen(text, wait_time=None, allow_skip=False, background_color=None):
    if background_color:
        win.color = background_color
    else:
        win.color = default_color

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


def show_text_with_countdown(text, countdown_seconds, allow_skip=False, background_color=None):
    if background_color:
        win.color = background_color
    else:
        win.color = default_color

    timer = core.Clock()

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


############# define provocation task function #############

def run_provocation_phase_with_timing(text, max_duration, background_color=None):
    """
    Displays a provocation screen for a maximum duration.

    Parameters:
    - text (str): Instruction text displayed during provocation.
    - max_duration (int): Maximum duration of provocation in seconds.
    - background_color (str): Background color for the screen.
    """
    if background_color:
        win.color = background_color
    else:
        win.color = default_color

    #play sound
    beep_tone.play()

    # Start clock and mark time
    provocation_timer = core.Clock()
    start_time = datetime.now()

    actual_duration = None

    while True:
        elapsed = provocation_timer.getTime()
        remaining = max_duration - elapsed
        if remaining <= 0:
            break

        # Draw provocation message (commented out timer text is with visible countdown)
        main_text = visual.TextStim(win, text=text, pos=(0, 100), color="white", height=30, wrapWidth=1000)
       # timer_text = visual.TextStim(win, text=f"{int(remaining)} sekunder", pos=(0, -60), color="white", height=30)

        main_text.draw()
      #  timer_text.draw()
        win.flip()

        keys = event.getKeys()
        check_for_quit(keys)

        if SPACE_KEY in keys:
            actual_duration = elapsed
            break

    end_time = datetime.now()
    beep_tone.play() #play at end of provocation phase

    # Calculate actual duration in seconds
    if actual_duration is None:
        actual_duration = max_duration

    return actual_duration, start_time.strftime("%H:%M:%S"), end_time.strftime("%H:%M:%S")


########### define tutorial function ###############

def run_tutorial(tutorial_data_list):
    """
    Displays tutorial text screens and runs practice trials for each trial type.

    Parameters:
    - tutorial_data_list (list): List to store data.
    """
    tutorial_start_time = datetime.now().strftime("%H:%M:%S")

    for i, text in enumerate(tutorial_texts):
        print(f"Tutorial screen {i+1} of {len(tutorial_texts)}")  # Optional debug
        show_text_screen(text, allow_skip=True)#, centered=False) 


    for i, trial_type in enumerate(tutorial_trial_types):
        print(f"Running Trial {i+1} — {trial_type.capitalize()}")

        # Get the current template
        practice_phases = trial_templates[trial_type]

        # get trial specific background color
        bg_color = trial_colors[trial_type]  

        show_text_with_countdown(practice_phases["anticipation"], countdown_seconds=5, background_color=bg_color)

        duration_sec, start_time, end_time = run_provocation_phase_with_timing(
            text=practice_phases["provocation"],
            max_duration=tutorial_provoke_duration,
            background_color=bg_color
        )
        print(f"Practice {trial_type} duration: {duration_sec} seconds")

        show_text_screen(practice_phases["recovery"], wait_time=4)

        # VAS questions
        vas_ratings = {}
        for idx in vas_questions_exp[trial_type]:
            rating = show_vas(idx["question"], idx["labels"])
            vas_ratings[idx["type"]] = rating
            print(f"VAS Response [{trial_type}]: {idx['type']} = {rating}")


        if save_tutorial_data:
            # Prepare trial data dictionary
            trial_data = {
                "participant_ID": participant_ID,
                "trial_number": (f"tutorial_{trial_type}_{i + 1}"),
                "trial_type": trial_type,
                "provocation_duration_sec": duration_sec,
                "provocation_start_time": start_time,
                "provocation_end_time": end_time
            }

            # Add VAS ratings to trial data
            trial_data.update(vas_ratings)

            tutorial_data.append(trial_data)
   
        show_text_screen(break_text0, wait_time= random_break) # intertrial interval

    # outro from tutorial text
    show_text_screen(break_text1, allow_skip=True) 



############### define experiment function ###############
def run_experiment(experiment_data_list):
    """
    Runs the main experiment, displaying text screens (with or without countdowns),
    and collecting VAS ratings for each trial type.

    Parameters:
    - experiment_data_list (list): List to store trial data.
    
    Returns:
    - experiment_data_list (list): Updated list with trial data.
    """
    show_text_screen(break_text2, wait_time=3)

    for i, trial_type in enumerate(trial_types):
        print(f"Running Trial {i+1} — {trial_type.capitalize()}")

        # Get the current template
        phases = trial_templates[trial_type]

        # get color
        bg_color = trial_colors[trial_type]  # Get the trial-specific color


        # Show anticipation, provocation, recovery
        show_text_with_countdown(phases["anticipation"], countdown_seconds=5, background_color=bg_color)

        #show_text_with_countdown(phases["provocation"], countdown_seconds=60, allow_skip=True, background_color=bg_color)

        # Run provocation and record timing
        duration_sec, start_time, end_time = run_provocation_phase_with_timing(
            text=phases["provocation"],
            max_duration=exp_provoke_duration,
            background_color=bg_color
        )

        print(f"Trial {i+1} — {trial_type.capitalize()} Duration: {duration_sec} seconds")

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
            "trial_type": trial_type,
            "provocation_duration_sec": duration_sec,
            "provocation_start_time": start_time,
            "provocation_end_time": end_time
        }

        # Add VAS ratings to trial data
        trial_data.update(vas_ratings)

        experiment_data.append(trial_data)

        show_text_screen(break_text0, wait_time=random_break)  # ITI


########## SAVE DATA FUNCTION ##########

def save_data(experiment_data, tutorial_data, vas_ratings_end):
    # Append the end-of-experiment VAS questions as a summary row
    end_row = {
        "participant_ID": participant_ID,
        "trial_number": "end",
        "trial_type": "end_questions"
    }
    end_row.update(vas_ratings_end)
    experiment_data.append(end_row)

    if save_tutorial_data:
        all_data = tutorial_data + experiment_data
    else:
        all_data = experiment_data

    df = pd.DataFrame(all_data)

    timestamp = experiment_start.strftime('%Y%m%d_%H%M')

    # Add metadata columns
    df["experiment_date"] = experiment_start.strftime("%Y-%m-%d")
    df["experiment_start_time"] = experiment_start.strftime("%H:%M:%S")
    df["experiment_end_time"] = experiment_end.strftime("%H:%M:%S")

    # Ensure 'data' directory exists
    data_folder = "data"
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)

    # Save DataFrame to CSV
    filename = f"recordID_{participant_ID}_provocation_{timestamp}.csv"
    filepath = os.path.join(data_folder, filename)
    df.to_csv(filepath, index=False)
    print(f"Data saved to {filename}")

# --------- MAIN PROGRAM ----------
experiment_start = datetime.now()

tutorial_data = []
experiment_data = []

if show_tutorial == 1:
    run_tutorial(tutorial_data)

# run experiment
run_experiment(experiment_data)

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
save_data(experiment_data, tutorial_data, vas_ratings_end)

win.close()
core.quit()

