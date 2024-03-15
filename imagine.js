function gpt(system_prompt, user_prompt, json) {

}


// pseudo-code
async function branch(tree, prompts) {
    // base condition
    
    prompts.forEach(prompt => {
        write_new_events(prompt)
        new_tree = plot2tree(new_events)
        new_tree = merge_tree(tree, new_tree)
        key_events = get_key_events(new_tree)
        prompts = generate_prompts(new_tree, key_events)
        branch(new_tree, prompts)
    });
    await Promise.forAll; 
}

input: og_plot
og_tree = plot2tree(og_plot)
key_events = get_key_events(og_tree)
prompts = generate_prompts(og_tree, key_events)
branch(tree, prompts)


await fetch(
    `https://api.openai.com/v1/chat/completions`,
    {
        body: JSON.stringify({
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": "Say this is a test!"}],
            "temperature": 0.7
        }),
        method: "POST",
        headers: {
            "content-type": "application/json",
            Authorization: "Bearer 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",
        },
            }
).then((response) => {
    if (response.ok) {
        response.json().then((json) => {
            console.log(json);
        });
    }
});

