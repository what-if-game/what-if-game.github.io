async function fetchStoryContent(storyTitle) {
    try {
        // Construct the URL from the storyTitle
        const url = `stories/${storyTitle.toLowerCase().replace(/ /g, '_')}/ink.txt`;
        
        // Await the fetch request
        const response = await fetch(url);
        
        // Await the text response
        const text = await response.text();
        
        // Logging the fetched text
        console.log(text);
        
        // Assigning the fetched text to storyContent
        return text; // Returning the text in case you need to use it outside the function
    } catch (error) {
        // Error handling
        console.error(error);
    }
}

async function main() {
    storyContent = await fetchStoryContent(storyTitle);
    console.log('story:');
    console.log(storyContent);
    const story = new inkjs.Compiler(storyContent).Compile();
    // story is an inkjs.Story that can be played right away
    
    // const jsonBytecode = story.ToJson();
    // // the generated json can be further re-used

    var storyContainer = document.querySelectorAll('#story')[0];

    function isAnimationEnabled() {
        return window.matchMedia('(prefers-reduced-motion: no-preference)').matches;
    }

    function showAfter(delay, el) {
        setTimeout(function() { el.style.opacity = 1.0 }, isAnimationEnabled() ? delay : 0);
    }

    function typingEffect(el, text, speed, i = 0) {
        if (i < text.length) {
            el.innerHTML += text.charAt(i);
            i++;
            setTimeout(() => typingEffect(el, text, speed, i), speed);
        } else {
            return;
        }
    }

    function scrollToBottom() {
        // If the user doesn't want animations, let them scroll manually
        if (!isAnimationEnabled()) {
            return;
        }
        var start = window.pageYOffset || document.documentElement.scrollTop || document.body.scrollTop || 0;
        var dist = document.body.scrollHeight - window.innerHeight - start;
        if( dist < 0 ) return;

        var duration = 300 + 300*dist/100;
        var startTime = null;
        function step(time) {
            if( startTime == null ) startTime = time;
            var t = (time-startTime) / duration;
            var lerp = 3*t*t - 2*t*t*t;
            window.scrollTo(0, start + lerp*dist);
            if( t < 1 ) requestAnimationFrame(step);
        }
        requestAnimationFrame(step);
    }

    function continueStory() {
        var paragraphIndex = 0;
        var delay = 0.0;
        let typingSpeed = 20 // smaller the faster
        // Generate story text - loop through available content
        while(story.canContinue) {

            // Get ink to generate the next paragraph
            var paragraphText = story.Continue();

            // Create paragraph element
            var paragraphElement = document.createElement('p');
            
            storyContainer.appendChild(paragraphElement);
            // typingEffect(paragraphElement, paragraphText)
            let totalTypingTime = paragraphText.length * typingSpeed;

            // Use a closure to ensure the correct timing for each paragraph
            
            ((element, text, speed, delayTime) => {
                setTimeout(() => {
                    typingEffect(element, text, speed);
                }, delayTime);
            })(paragraphElement, paragraphText, typingSpeed, delay);

            delay += totalTypingTime + 2000;
            // Fade in paragraph after a short delay
            // showAfter(delay, paragraphElement);

            // delay += 2000;
        }

        // Create HTML choices from ink choices
        story.currentChoices.forEach(function(choice) {

            // Create paragraph with anchor element
            var choiceParagraphElement = document.createElement('p');
            choiceParagraphElement.classList.add("choice");
            choiceParagraphElement.innerHTML = `<a href='#'>${choice.text}</a>`
            choiceParagraphElement.style.opacity = 0.0
            storyContainer.appendChild(choiceParagraphElement);

            // Fade choice in after a short delay
            showAfter(delay, choiceParagraphElement);
            // delay += 1000.0;

            // Click on choice
            var choiceAnchorEl = choiceParagraphElement.querySelectorAll("a")[0];
            choiceAnchorEl.addEventListener("click", function(event) {

                // Don't follow <a> link
                event.preventDefault();

                // Remove all existing choices
                var existingChoices = storyContainer.querySelectorAll('p');
                for(var i=0; i<existingChoices.length; i++) {
                    var c = existingChoices[i];
                    c.parentNode.removeChild(c);
                }

                // Tell the story where to go next
                story.ChooseChoiceIndex(choice.index);

                // Aaand loop
                continueStory();
            });
        });

        scrollToBottom();
    }

    continueStory();

}
main();
