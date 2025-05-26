##### Abdominal Tensing Task #####
# This script is used to run the abdominal tensing task experiment
# Created by: Sigrid Bom Nielsen, PhD-student at Aarhus University, Denmark
# Date: 2025-04-01

# comments
#-
#-
#-

#------------------------- PACKAGES -------------------------#

# importing packages
import pandas as pd
import sys, random, os
from psychopy import visual, core, event, sound
from datetime import datetime
# if you have issues installing psychopy, install the packages from dependencies.txt
import pygame

###### ----------------- setting variables ------------------ ######

trials_number = 6  # trial number in total - must be an even number for balanced randomization
#trial_types = ["abdominal", "hands"] * (NUM_TRIALS // 2)
#random.shuffle(trial_types)

tutorial_trial_types = ["hands", "abdominal"]  # for the tutorial, we only use one of each type and we start with hands


# background colors for each trial type and default color
trial_colors = {
    "hands": "green",
    "abdominal": "blue"
}

default_color = "grey"

save_tutorial_data = True  # Set to True if you want to save tutorial data, False otherwise

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
        "Velkommen til mave-spændings-eksperimentet. \n\nTryk på mellemrumstasten for at fortsætte.", 

        "I dette eksperiment vil du blive bedt om skiftevis at knytte dine hænder eller spænde i dine mavemuskler. "
        "Du vil blive bedt om at knytte dine hænder eller spænde dine mavemuskler i et minut.\n\n"
        "Hvis du ikke kan gøre det så længe, tryk på mellemrumstasten for at vise, at du er stoppet.\n\n"
        "Du vil derefter blive bedt om at svare på nogle spørgsmål om, hvordan det føltes. Tryk på mellemrumstasten for at fortsætte.",

        "Vi starter med en prøverunde.\n\n"# Følg instruktionerne på skærmen.\n\n"
        "Når skærmen er grøn, skal du knytte dine hænder.\n Når skærmen er blå, skal du spænde dine mavemuskler.\n\n"
        "Når du skal knytte dine hænder eller spænde dine mavemuskler, vil du høre en kort bip tone. Du hører lyden igen, når der er gået et minut, eller hvis du stopper før tid.\n\n"
        "I prøverunden skal du kun knytte dine hænder eller spænde dine mavemuskler i 30 sekunder.\n\n"
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

###### ----------------- Create window and save keys ------------------ ######
experiment_start = datetime.now()

tutorial_data = []
experiment_data = []

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

def run_provocation_phase_with_timing(text, max_duration=60, background_color=None):
    """
    Displays a provocation screen for a maximum duration.
    Returns the duration the participant held the tension, and start/end timestamps.
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

        # Draw provocation message and countdown
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

def run_tutorial(tut_text_list):
    tutorial_start_time = datetime.now().strftime("%H:%M:%S")

    for i, text in enumerate(tut_text_list):
        print(f"Tutorial screen {i+1} of {len(tut_text_list)}")  # Optional debug
        show_text_screen(text, allow_skip=True) 


    for i, trial_type in enumerate(tutorial_trial_types):
        print(f"Running Trial {i+1} — {trial_type.capitalize()}")

        # Get the current template
        practice_phases = trial_templates[trial_type]

        # get color
        bg_color = trial_colors[trial_type]  # Get the trial-specific color

        show_text_with_countdown(practice_phases["anticipation"], countdown_seconds=5, background_color=bg_color)

        duration_sec, start_time, end_time = run_provocation_phase_with_timing(
            text=practice_phases["provocation"],
            max_duration=60,
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

    # run hands
#    practice_phases = trial_templates["hands"]
   # show_text_with_countdown(practice_phases["anticipation"], countdown_seconds=5, background_color=trial_colors["hands"])

    # Run provocation and record timing
    # duration_sec, start_time, end_time = run_provocation_phase_with_timing(
    #         text=practice_phases["provocation"],
    #         max_duration=60,
    #         background_color=trial_colors["hands"])

    # print(f"Practice Hands Duration: {duration_sec} seconds")

    #show_text_with_countdown(practice_phases["provocation"], countdown_seconds=30, allow_skip=True, background_color='green')
    # show_text_screen(practice_phases["recovery"], wait_time=4)

    # # # VAS questions
    # for idx in vas_questions_exp["hands"]:
    #     rating = show_vas(idx["question"], idx["labels"])
    #     print(f"VAS Response [hands]: {idx['type']} = {rating}")


   # show_text_screen(break_text0, wait_time= random_break) # intertrial interval

    # run abdominal
    # practice_phases = trial_templates["abdominal"]
    # show_text_with_countdown(practice_phases["anticipation"], countdown_seconds=5, background_color=trial_colors["abdominal"])
    # #show_text_with_countdown(practice_phases["provocation"], countdown_seconds=30, allow_skip=True, background_color='blue')

    # duration_sec, start_time, end_time = run_provocation_phase_with_timing(
    #         text=practice_phases["provocation"],
    #         max_duration=60,
    #         background_color=trial_colors["abdominal"])
    
    # print(f"Practice Abdominal Duration: {duration_sec} seconds")  # Optional debug

    # show_text_screen(practice_phases["recovery"], wait_time=4)

    # # VAS questions
    # for idx in vas_questions_exp["abdominal"]:
    #     rating = show_vas(idx["question"], idx["labels"])
    #     print(f"VAS Response [abdominal]: {idx['type']} = {rating}")

    # outro from tutorial text
    # show_text_screen(break_text1, allow_skip=True) 


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

        #show_text_with_countdown(phases["provocation"], countdown_seconds=60, allow_skip=True, background_color=bg_color)

        # Run provocation and record timing
        duration_sec, start_time, end_time = run_provocation_phase_with_timing(
            text=phases["provocation"],
            max_duration=60,
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

    if save_tutorial_data:
        all_data = tutorial_data + experiment_data
    else:
        all_data = experiment_data

    df = pd.DataFrame(all_data)
    #df = pd.DataFrame(experiment_data)

    timestamp = experiment_start.strftime('%Y%m%d_%H%M%S')

    # Add metadata columns
    df["experiment_date"] = experiment_start.strftime("%Y-%m-%d")
    df["experiment_start_time"] = experiment_start.strftime("%H:%M:%S")
    df["experiment_end_time"] = experiment_end.strftime("%H:%M:%S")

    # Ensure 'data' directory exists
    data_folder = "data"
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)

    filename = f"provocation_participant_{participant_ID}_{timestamp}.csv"
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

