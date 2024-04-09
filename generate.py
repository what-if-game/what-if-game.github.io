from openai import OpenAI
import json
from tqdm import tqdm

def plot2tree(plot, char_name, num_nodes=""):
    """
    Convert a plot to a story branching tree.

    Args:
        plot: the plot of a movie
        num_nodes: the number of story nodes in the output tree

    Returns:
        A story branching tree that summarizes the plot
    """

    JSON_SCHEMA = f"""
{{
    "node_1": {{
      "state": "<initial state of {char_name}>",    /* The initial state of the main character. This should NOT contain any important plot point. */
      "goal": "<goal of {char_name} given the current state>",    /* The goal the main character is attempting to reach in the current state. This should starts with 'To ...' */
      "decision": "<key decision taken by {char_name} that propels the story forward>", /* The key decision taken by {char_name} given the state and goal, starting with '{char_name} decides to ...'. */
      "edgeEvents": [                      /* List of specific events resulting from the key decision and leading up to the state of next node. Each event should be a complete sentence with all involved characters */
        "<repeat key decision taken by {char_name} that propels the story forward, starting with '{char_name} decides to ...'>",
        "<event resulting from the key decision and leading to next state>",
        "<next state of {char_name} resulting from the previous events>"
      ],
      "alternate_decision": "<an alternate decision {char_name} could have made given the same state and goal that would have led to a different storyline, starting with '{char_name} decides to ...'>"

    }},
    "node_2":{{
      "state": "<state of the character resulting from the previous node's edgeEvents>",    /* The current state of the main character, resulted from the previous node's edgeEvents. This should NOT contain any important plot point. */
      "goal": "<goal of the character given the current state>",    /* The goal the main character is attempting to reach in the current state. This should starts with 'To ...' */
      "decision": "<key decision taken by {char_name} that propels the story forward>", /* The key decision taken by {char_name} given the state and goal, starting with '{char_name} decides to ...' */
      "edgeEvents": [                      /* List of specific events resulting from the key decision and leading up to the state of next node. Each event should be a complete sentence with all involved characters */
        "<repeat key decision taken by {char_name} that propels the story forward, starting with '{char_name} decides to ...'>",
        "<event resulting from the key decision and leading to next state>",
        "<next state of {char_name} resulting from the previous events>"
      ],
      "alternate_decision": "<an alternate decision {char_name} could have made given the same state and goal that would have led to a different storyline, starting with '{char_name} decides to ...'>"
    }},

    /* ...continue for all {num_nodes} nodes... */

    "node_n": {{     /* n is the total number of nodes */
      "state": "<state of the character resulting from previous node's edgeEvents>",  /* The current state of the main character, resulted from the previous node's edgeEvents. This should NOT contain any important plot point. */
      "goal": "<final character goal given the current state>",    /* The goal the main character is attempting to reach in the final state. This should starts with 'To ...' */
      "decision": "<key decision taken by {char_name} that propels the story forward>", /* The key decision taken by {char_name} given the state and goal, starting with '{char_name} decides to ...' */
      "edgeEvents": [     /* List of final events resulting from the key decision and leading to the end of the story. Each event should be a complete sentence with all involved characters */
        "<repeat key decision taken by {char_name} leading to end of story, starting with '{char_name} decides to ...'>",
        "<event resulting from the key decision and leading to end of story>",
        "<final state of {char_name} resulting from the previous events>"
      ],
      "alternate_decision": "<an alternate decision {char_name} could have made given the same state and goal that would have led to a different storyline, starting with '{char_name} decides to ...'>"
    }}
}}
"""

    response = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        response_format={"type": "json_object"},
        seed=42,
        messages=[
            {"role": "system", "content": "# You are a helpful fiction writer assistant."},
            {"role": "user", "content": f"{plot}\nSummarize the plot above into a plot tree of {'at most 6' if num_nodes == '' else num_nodes} nodes with each node containing the state and goal of {char_name},\
            and the key decision that propels the story forward. Each edge should contain a list of events \
            that lead {char_name} to the state of next node. Also, Given the same state and goal of {char_name}, imagine an alternate decision that would have led {char_name} to a different storyline.\
            Output in JSON format with schema: {JSON_SCHEMA}. Make sure that all important plot points are included in 'edgeEvents' but not in 'state'"},
        ]
    )
    tree = response.choices[0].message.content
    return json.loads(tree)

def get_all_events(storyline):
    event_list = []
    for i in storyline.keys():
        event_list.extend(storyline[i]['edgeEvents'])
    return event_list

def get_key_events(events):
    JSON_SCHEMA = """
{
    "inciting_incident": {
        "eventId": "the event number",
        "event": "the event corresponding to the inciting incident"
    },
    "crisis": {
        "eventId": "the event number",
        "event": "the event corresponding to the crisis"
    }
    "climax": {
        "eventId": "the event number",
        "event": "the event corresponding to the climax"
    }
}
"""
    response = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        response_format={"type": "json_object"},
        seed=42,
        messages=[
            {"role": "system", "content": f"Here are some definitions in the context of three-act story structure:\
             The inciting incident is an event that pulls the protagonist out of their normal world and into the main action of the story. It is the turning point between Act One and Act Two.\
             The crisis is the moment when the protagonist faces their greatest challenge or obstacle, leading directly to the climax of the story. It is the turning point between Act Two and Act Three.\
             The climax is the climactic confrontation in which the hero faces a point of no return: they must either prevail or perish. It occurs in Act Three and should have the peak tension of the story.\
             You will be given a list of events from a movie plot. Your task is to identify the inciting incident, crisis, and climax. Output in JSON format with schema: {JSON_SCHEMA}."},
            {"role": "user", "content": f"{events}"},
        ]
    )
    key_events = response.choices[0].message.content
    return json.loads(key_events)

def generate_prompt(all_events, key_events, storyline, branching_node, charname):
    key_event_indices = [i['eventId'] for i in list(key_events.values())]
    key_event_list = [i['event'] for i in list(key_events.values())]

    branching_event = (branching_node - 1) * 3 + 1
    if branching_event <= int(key_event_indices[0]):
        mpp = key_event_list
    elif branching_event <= int(key_event_indices[1]):
        mpp = key_event_list[1:]
    elif branching_event <= int(key_event_indices[2]):
        mpp = key_event_list[2]
    else:
        mpp = 'the rest of the story'
    JSON_SCHEMA = f"""
{{
    "branching_event_number": branching_event,
    "original_decision" : storyline[f"node_{branching_node}"]['decision'],
    "alternate_decision" : storyline[f"node_{branching_node}"]['alternate_decision'],
    "new_story_length": (len(storyline) - branching_node) * 3,
    "major_plot_points" : mpp,
    "prompt": f"TODO: <a prompt for ChatGPT for every branching point above with following requirements:\
            1. Ask to use the original storyline as a reference to write an alternate storyline that branches out at event {branching_event} if {char_name} {storyline[f'node_{branching_node}']['alternate_decision']} instead of {storyline[f'node_{branching_node}']['decision']}.\
            2. Provide 5 thought-provoking concrete guiding questions as potential directions to explore that expand the following:\n\
                a. How would alternate decision change or replace {mpp}?\
                b. How would {char_name} make key decisions that overcome new challenges and propel the story forward?\
            3. Describe what an ideal alternate storyline should look like.\
            4. Ask to output the alternate storyline as a list of {(len(storyline) - branching_node + 1) * 3} events that has {storyline[f'node_{branching_node}']['alternate_decision']} as the first event>"
}}
"""
    response = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        response_format={"type": "json_object"},
        seed=42,
        messages=[
            {"role": "system", "content": "# You are an expert in prompting ChatGPT."},
            {"role": "user", "content": f"Original storyline:{all_events}\n\
             Write a prompt for ChatGPT with following requirements:\
             1. Ask to use the original storyline as a reference to write an alternate storyline that branches out at event {branching_event} if {char_name} {storyline[f'node_{branching_node}']['alternate_decision']} instead of {storyline[f'node_{branching_node}']['decision']}.\
             2. Provide 5 thought-provoking concrete guiding questions as potential directions to explore that expand the following:\n\
                a. How would alternate decision change or replace {mpp}?\
                b. How would {char_name} make key decisions that overcome new challenges and propel the story forward?\
             3. Describe what an ideal alternate storyline should look like.\
             4. Ask to output the alternate storyline as a list of {(len(storyline) - branching_node + 1) * 3} events that has {storyline[f'node_{branching_node}']['alternate_decision']} as the first event.\
             \nOutput the prompt with following JSON schema: {JSON_SCHEMA}"}
        ]
    )
    prompt = response.choices[0].message.content
    return json.loads(prompt)['prompt']

def write_new_storyline(all_events, prompt):
    JSON_SCHEMA = """
{
    "events": {
        "event number": "an event in the new storyline"
    }
}
"""
    response = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        response_format={"type": "json_object"},
        seed=42,
        messages=[
            {"role": "system", "content": "# You are a helpful fiction writer assistant."},
            {"role": "user", "content": f"Original storyline:\n{all_events}\n\n{prompt}\nOutput in JSON format with schema: {JSON_SCHEMA}."}
        ]
    )
    new_storyline = response.choices[0].message.content
    return list(json.loads(new_storyline)["events"].values())

def merge_tree(og_storyline, new_storyline, branching_node):
    merge_tree = {}
    for i in range(1, branching_node + len(new_storyline)):
        if i < branching_node:
            merge_tree[f'node_{i}'] = og_storyline[f'node_{i}']
        elif i == branching_node:
            merged_node = og_storyline[f'node_{branching_node}']
            merged_node['decision'] = new_storyline[f'node_1']['decision']
            merged_node['edgeEvents'] = new_storyline[f'node_1']['edgeEvents']
            merged_node['alternate_decision'] = new_storyline[f'node_1']['alternate_decision']
            merge_tree[f'node_{i}'] = merged_node
        else:
            merge_tree[f'node_{i}'] = new_storyline[f'node_{i-branching_node+1}']
    return merge_tree

def narrate(node, char_name, is_ending=False):
    if not is_ending:
        JSON_SCHEMA = """
{
    "paragraphs": "<Narrate the three events as three short paragraphs using second-person perspective, then transit to the state and goal of the player. Use newline characters between paragraphs>",
    "button_text_1": "<short button text for original decision>",
    "button_text_2": "<short button text for alternate decision>"
}
"""
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            response_format={"type": "json_object"},
            seed=42,
            messages=[
                {"role": "system", "content": f"# You are  writing a Choose Your Own Adventure style interactive fiction game in which the player is {char_name}.\
                You will be given a list of events, the resulting state and goal of the character, and two decisions.\
                Do the following:\
                    1. Narrate each event in a paragraph. You should never mention {char_name} but always use the second-person perspective.\
                    2. Seemlessly transit to the state and goal of the player.\
                    3. Provide two button-text reflects the two decisions. \
                Output in JSON with schema: {JSON_SCHEMA}"},
                {"role": "user", "content": f"{node}"}
            ]
        )
    else:
        JSON_SCHEMA = """
{
    "paragraphs": "<Narrate the three events as three short paragraphs using second-person perspective, then transit to the ending of the story. Use newline characters between paragraphs>",
}
"""
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            response_format={"type": "json_object"},
            seed=42,
            messages=[
                {"role": "system", "content": f"# You are writing a Choose Your Own Adventure style interactive fiction game in which the player is {char_name}.\
                You will be given a list of events.\
                Do the following:\
                    1. Narrate each event in a paragraph. You should never mention {char_name} but always use the second-person perspective.\
                    2. Seemlessly transit to the ending of the story.\
                    3. On a separate line, print out 'THE END'.\
                Output in JSON with schema: {JSON_SCHEMA}"},
                {"role": "user", "content": f"{node}"}
            ]
        )
    narration = response.choices[0].message.content
    return json.loads(narration)

def reorder_tree(tree):
    reordered_tree = []
    prev_events = tree['node_1']['edgeEvents']
    if len(tree) > 1:
        for k in sorted(tree.keys())[1:]:
            reordered_tree.append({
                "events": prev_events,
                "state": tree[k]['state'],
                "goal": tree[k]['goal'],
                "original_decision": tree[k]['decision'],
                "alternate_decision": tree[k]['alternate_decision']
            })
            prev_events = tree[k]['edgeEvents']
    reordered_tree.append({
        "events": prev_events,
        "state": None,
        "goal": None,
        "original_decision": None,
        "alternate_decision": None
    })
    return reordered_tree

def add_ink_and_chart(reordered_tree, char_name, prefices, ink, chart):
    nl = '\n'
    if len(reordered_tree) > 1:
        for i, n in enumerate(reordered_tree[:-1]):
            ink.append(f"== {prefices[i]} ==")
            narration = narrate(n, char_name)
            ink.append(f"{narration['paragraphs']}")
            ink.append(f"+ [{narration['button_text_1']}] -> {prefices[i]}L")
            ink.append(f"+ [{narration['button_text_2']}] -> {prefices[i]}R")
            chart.append(f"{prefices[i]}E({nl.join(n['events'])}) --> {prefices[i]}")
            chart.append(f"{prefices[i]}[[S: {n['state']}{nl}G: {n['goal']}]] --> |{narration['button_text_1']}|{prefices[i]}LE")
            chart.append(f"{prefices[i]} --> |{narration['button_text_2']}|{prefices[i]}RE")


    ink.append(f"== {prefices[-1]} ==")
    narration = narrate(reordered_tree[-1], char_name, is_ending=True)
    ink.append(f"{narration['paragraphs']}")
    ink.append('-> END')
    chart.append(f"{prefices[-1]}E({nl.join(reordered_tree[-1]['events'])})")

def branch(tree, tree_labels, char_name, max_len, ink, chart, pbar):
    if len(tree_labels[0]) == max_len:
        return
    all_events = get_all_events(tree)
    key_events = get_key_events(all_events)
    # prompts = generate_prompts(all_events, key_events, tree, len(tree_labels[0]) + 1, char_name)
    prompts = []
    for i in range(len(tree_labels[0]) + 1, max_len + 1):
        # print(i)
        prompts.append(generate_prompt(all_events, key_events, tree, i, char_name))
        # prompts.append(f"generate a new story of {j * 3} events")
    # print(f"{len(prompts)} prompts")
    # print(prompts)
    for i, prefix in enumerate(tree_labels):
        if len(prefix) == max_len:
            break
        paths = [prefix + 'R']
        while len(paths[-1]) < max_len:
            paths.append(paths[-1] + 'L')
        # print(paths)

        new_storyline = write_new_storyline(all_events, prompts[i])
        print(new_storyline)
        # print(f"{len(new_storyline)} new events")
        new_tree = plot2tree(new_storyline, char_name, int(len(new_storyline) / 3))
        while len(new_tree) != int(len(new_storyline) / 3):
            new_tree = plot2tree(new_storyline, char_name, int(len(new_storyline) / 3))
        # print(f"{len(new_tree)} nodes in new tree")
        if len(paths[0]) - 1 == 0:
            reordered_tree = reorder_tree(new_tree)
        else:
            reordered_tree = reorder_tree(new_tree)
        # print(f"{len(reordered_tree)} narrations")
        add_ink_and_chart(reordered_tree, char_name, paths, ink, chart)
        pbar.update(1)
        new_tree = merge_tree(tree, new_tree, len(paths[0]))
        # print(f"{len(new_tree)} nodes in new merged tree")
        branch(new_tree, paths, char_name, max_len, ink, chart, pbar)

def generate(og_plot, char_name, num_nodes):
    og_tree = plot2tree(og_plot, char_name, num_nodes)
    ink = ["-> S", "== S =="]
    nl = '\n'
    reordered_tree = reorder_tree(og_tree)
    tree_labels = ['L'*i for i in range(1, num_nodes + 1)]
    start_node = {
        "events": None,
        "state": og_tree['node_1']['state'],
        "goal": og_tree['node_1']['goal'],
        "original_decision": og_tree['node_1']['decision'],
        "alternate_decision": og_tree['node_1']['alternate_decision']
    }
    narration = narrate(start_node, char_name)
    ink.append(f"{narration['paragraphs']}")
    ink.append(f"+ [{narration['button_text_1']}] -> L")
    ink.append(f"+ [{narration['button_text_2']}] -> R")
    chart = [f"S[[S: {start_node['state']}{nl}G: {start_node['goal']}]] --> |{narration['button_text_1']}|LE"]
    chart.append(f"S[[S: {start_node['state']}{nl}G: {start_node['goal']}]] --> |{narration['button_text_2']}|RE")
    add_ink_and_chart(reordered_tree, char_name, tree_labels, ink, chart)

    pbar = tqdm(total=num_nodes*num_nodes)
    pbar.update(1)
    branch(og_tree, ['L'*i for i in range(num_nodes + 1)], char_name, len(tree_labels), ink, chart, pbar)

    return ink, chart

client = OpenAI(
    api_key=input('Enter your OpenAI API Key:\n'),
)

char_name = "Natasha Romanoff"
story_name = "Black Widow"
og_plot = """
In 1995, super soldier Alexei Shostakov (David Harbour) (The Russian super-soldier counterpart to Captain America and a father-figure to Romanoff and Belova) and Black Widow Melina Vostokoff (Rachel Weisz) (A seasoned spy trained in the Red Room as a Black Widow and a mother-figure to Romanoff and Belova who is now one of the Red Room's lead scientists) work as Russian undercover agents, posing as a family in Ohio with Natasha Romanoff (Scarlett Johansson) and Yelena Belova (Florence Pugh) as their daughters.
They steal S.H.I.E.L.D. intel and escape to Cuba where their boss, General Dreykov (Ray Winstone) (Russian General and head of the Red Room Program), has Romanoff and Belova taken to the Red Room for training. Yelena is happy to be back, but Natasha is distraught at leaving Ohio and doesn't want to go back into the Red Room program. Years pass, during which Shostakov is imprisoned in Russia while Romanoff defects to S.H.I.E.L.D. after bombing Dreykov's Budapest office and apparently killing him and his young daughter Antonia (Olga Kurylenko).
In 2016, Romanoff is a fugitive for violating the Sokovia Accords (The Sokovia Accords are a set of legal documents designed to regulate the activities of enhanced individuals, specifically for those who work for either government agencies such as S.H.I.E.L.D. or for private organizations such as the Avengers. Established by the United Nations and ratified by 117 nations, the accords serve as a "middle point" between the Avengers' desire to secure world peace and the international community's concern over the repercussions of the Avengers' actions).
The Sokovia Accords caused a schism in the Avengers. While Tony Stark supported the Accords due to his role in the Ultron Offensive, Steve Rogers recognized that the government having power over potential missions may be a terrible idea in an emergency and disliked the authoritarian nature of its stipulations, noting that signing the Accords would be "surrendering the right to choose". The schism came to a head when Helmut Zemo framed Bucky Barnes for a terrorist attack that occurred during the signing of the Accords.
Combined with Zemo's exploitation of the schism, the Accords tore the Avengers apart, causing Stark's pro-Accords faction and Rogers' anti-Accords faction to destroy an airport as the former attempted to arrest the latter. The Accords caused the anti-Accords faction and Natasha Romanoff, who had been pro-Accords but betrayed Stark's faction knowing that Rogers would never stand down, to either become fugitives or be placed under house arrest, ruining any chance of coordinated defense.
She escapes from U.S. Secretary of State Thaddeus Ross (William Hurt) and flees to a safe-house in Norway supplied by Rick Mason (O-T Fagbenle) (An ally from Romanoff's S.H.I.E.L.D. past who is romantically interested in her). Meanwhile, Belova kills a rogue former Black Widow but comes in contact with a synthetic gas that neutralizes the Red Room's chemical mind-control agent. Belova removes her own tracker, sends antidote vials to Romanoff, hoping she and the Avengers can free the other Widows, and goes into hiding.
When Romanoff is unknowingly driving with the vials in her car, Red Room agent Taskmaster attacks her. Romanoff realizes that the Taskmaster is interested in a case, and escapes from Taskmaster and finds that the vials came from Belova (it was collected by Mason from Natasha's hideout in Budapest). There she finds Belova who reveals that Dreykov is alive, and the Red Room is still active. Black Widows and Taskmaster attack them, but Romanoff and Belova evade them and meet with Mason, who supplies them with a helicopter. Belova says that the antidote was created by a Black Widow from Melina's generation. Belova says Dreykov has killed many little girls (only 1 in 20 survives the training, the rest he kills), and the black widow program needs to stop.
Romanoff and Belova break Shostakov out of prison (he was imprisoned by Dreykov, but he doesn't know why) to learn Dreykov's location, and he directs them to Vostokoff who lives on a farm outside Saint Petersburg. There she is refining the chemical mind control process used on the Widows (This is what Shostakov and Melina has stolen from SHEILD in the first place, all those yrs ago). Belova tells Melina that her mind control chemicals were used on her, and she only managed to get out because of the antidote, while Natasha abandoned her. Melina also tells Natasha that she was not abandoned by her parents, she was selected by a program that assessed genetic potential in infants, and her parents were paid off. But her mom kept looking for her, threatening the exposure of the Red room, so Dreykov had her killed
Vostokoff alerts Dreykov and his agents arrive to take them, but Romanoff convinces Vostokoff to help them (by informing her how her mind control research has been used to kill and maim Soviet girls all over the world) and the pair use face mask technology to switch places. The Taskmaster arrives, everyone is sedated and taken to the Red room, which is a floating city in the sky.
At the Red Room, Vostokoff frees Shostakov and Belova from their restraints. Dreykov sees through Romanoff's disguise and reveals that Taskmaster is Antonia, who suffered damage severe enough that Dreykov had to put technology in her head to save her, in turn creating the perfect soldier, capable of mimicking the actions & fighting styles of anyone she sees. Romanoff is unable to attack Dreykov due to a pheromone lock installed in every Widow but negates that by breaking her own nose and severing a nerve in her nasal passage. Shostakov battles Taskmaster while Vostokoff takes out one of the facility's engines. They then lock Taskmaster in a cell.
Dreykov escapes as other Black Widows attack Romanoff, but Belova exposes them to the antidote. Romanoff copies the locations of other Widows worldwide from Dreykov's computer as the facility begins to explode and fall. She retrieves two surviving antidote vials and frees Taskmaster from the locked cell.
Vostokoff and Shostakov escape via a plane (which loses control after they lose their vertical stabilizer and hence, they can't get back to the red room to rescue the girls) while Belova takes out Dreykov's aircraft (by destroying its engine with a pole, by the explosion throws her off the exploding deck of the Red room), killing him. Romanoff, who was watching this, jumps after her. In free-fall, Romanoff gives Belova a parachute before battling Taskmaster. After landing, Romanoff uses one antidote vial on Taskmaster and gives the other to Belova along with the locations of the other mind-controlled Widows so she can find and free them. Belova, Vostokoff, and Shostakov say goodbye to Romanoff and leave with Antonia and the freed Widows. Two weeks later, Mason supplies Romanoff with a Quinjet to use in freeing the imprisoned Avengers.
"""
num_nodes = 4
ink, chart = generate(og_plot, char_name, num_nodes)
with open(f'stories/{story_name.lower().replace(' ', '_')}/ink.txt', 'w+') as file:
    file.write('\n'.join(ink))

with open(f'stories/{story_name.lower().replace(' ', '_')}/chart.txt', 'w+') as file:
    file.write('\n'.join(chart))

print('finished')