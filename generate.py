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

char_name = "Scott Lang"
story_name = "Ant Man"
og_plot = """
In 1989, scientist Hank Pym (Michael Douglas) resigns from S.H.I.E.L.D. (led by Howard (John Slattery) and Peggy (Hayley Atwell)) after discovering their attempt to replicate his Ant-Man shrinking technology. Believing the technology is dangerous, Pym vows to hide it as long as he lives. Mitchell Carson wanted to force Hank to surrender the technology but is stopped by Howard and Peggy. Pym had developed the Pym particle which reduces the distance between atoms while increasing density and strength.
In the present day, Pym's estranged daughter, Hope Van Dyne (Evangeline Lilly), and former protege, Darren Cross (Corey Stoll), have forced him out of his company, Pym Technologies. Cross is close to perfecting a shrinking suit of his own, the Yellowjacket, which horrifies Pym. The Yellowjacket is a highly weapon laden version of his own shrinking suit and can have devastating consequences, if put into production. Unknown to Darren, Hope is spying for Pym and wants Pym to give her his original suit to defeat Darren. But Pym steadily refuses to do that & asks Hope to consider his suggested alternative. However, Darren is having difficulty in achieving a stable molecular reduction, leading to his organic test subjects being reduced to a gooey mass of cells. Eventually, he succeeds.
Upon his release from prison, well-meaning thief Scott Lang (Paul Rudd) moves in with his old cellmate, Luis (Michael Pena). Luis's roommates are Kurt (David Dastmalchian), who is a computer wizard & Dave (Tip "T.I." Harris) a pro lock smith. Lang has a master's in electrical engineering and yet cannot land a job due to his past record and has to serve at a Baskin Robbins. While visiting his daughter Cassie (Abby Ryder Fortson) unannounced, Lang is rebuked by his former wife Maggie (Judy Greer) and her police-detective fiance, Paxton (Bobby Cannavale), for not providing child support. Maggie asks Lang to get an apartment and to pay child support before he is allowed his visitation rights with Cassie.
Unable to hold a job because of his criminal record (Lang lies about his past to get the job but is fired whenever his background check is completed), Lang agrees to join Luis' crew and commit a burglary. Lang breaks into a house and cracks its safe, but only finds what he believes to be an old motorcycle suit, which he takes home. Unknown to Lang, the entire burglary was being observed by an ant with a micro-camera on it, which was relaying a live feed to Pym. After trying the suit on, Lang accidentally shrinks himself to the size of an insect. Terrified by the experience (during which Pym speaks to Lang via his helmet), he returns the suit to the house, but is arrested on the way out. Pym, the homeowner, visits Lang in jail and smuggles the suit into his cell to help him break out with the assistance of ants and flying insects.
At his home, Pym, who manipulated Lang through an unknowing Luis into stealing the suit as a test, wants Lang to become the new Ant-Man to steal the Yellowjacket from Cross. Pym says that he generates Electro-magnetic waves to stimulate the ant's olfactory nerves and is thus able to speak to them and get them to obey his commands.
Hope still believes that she can defeat Darren, but Pym is afraid to lose her as he did her mother. Pym explains to Lang that he designed a formula 40 years ago to shrink humans inside his suit. But he hid the formula as it was dangerous. He started his own company, Pym tech, & took Darren on as his protege. With time Darren suspected the existence of Pym's formula. When Pym did not cooperate with Darre, he voted Pym out of his own company.
Hope was angry with Pym for the death of her mother & helped Darren. But then she came back to Pym when she saw that Darren was loco. Pym's plan is to train Lang to use the suit & to break into Darren's lab, steal his suit & destroy all the data. Pym says that his specially designed helmet helps protect the brain chemistry, something that Darren has ignored in the design of his suit.
Having been spying on Cross after discovering his intentions, Hope helps Pym train Lang to fight in the suit and to control ants. While Hope harbors resentment towards Pym about her mother Janet's (Hayley Lovitt) death, he reveals that Janet, known as the Wasp, disappeared into a subatomic quantum realm to disable a Soviet nuclear missile (it was headed for the US and the only way to disable it was to go subatomic through solid titanium. Pym's own regulator was damaged, and so Janet stepped up). Pym warns Lang that he could suffer a similar fate if he overrides his suit's regulator. They send him to steal a device that will aid their heist from the Avengers' headquarters, where he briefly fights Sam Wilson/Falcon (Anthony Mackie).
Cross perfects the Yellowjacket and hosts an unveiling ceremony at Pym Technologies' headquarters. Lang, along with his crew and a swarm of flying ants, infiltrates the building during the event, sabotages the company's servers, and plants explosives. When he attempts to steal the Yellowjacket, he, along with Pym and Hope, are captured by Cross, who intends to sell both the Yellowjacket and Ant-Man suits to Hydra, led by former S.H.I.E.L.D officer Mitchell Carson (Martin Donovan). Lang breaks free and he and Hope dispatch most of the Hydra agents, though Carson is able to flee with a vial of Cross' particles. Lang pursues Cross as he escapes, while the explosives detonate, imploding the building.
Cross dons the Yellowjacket and attacks Lang before Lang is arrested by Paxton. His mind addled by the imperfect shrinking technology, Cross takes Cassie hostage to lure Lang into another fight. Lang overrides the regulator and shrinks to subatomic size to penetrate Cross' suit and sabotage it to shrink uncontrollably, killing Cross. Lang disappears into the quantum realm but manages to reverse the effects and returns to the macroscopic world.
In gratitude for Lang's heroism, Paxton covers for Lang to keep him out of prison. Seeing that Lang survived and returned from the quantum realm, Pym wonders if his wife is alive as well. Later, Lang meets up with Luis, who tells him that Wilson is looking for him.
"""
num_nodes = 4
ink, chart = generate(og_plot, char_name, num_nodes)
with open(f'stories/{story_name.lower().replace(' ', '_')}/ink.txt', 'w+') as file:
    file.write('\n'.join(ink))

with open(f'stories/{story_name.lower().replace(' ', '_')}/chart.txt', 'w+') as file:
    file.write('\n'.join(chart))

print('finished')