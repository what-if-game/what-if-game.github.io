async function fetchStoryContent(storyTitle) {
    try {
        // Construct the URL from the storyTitle
        const url = `/stories/${storyTitle.toLowerCase().replace(/ /g, '_')}/ink.txt`;
        
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

var storyContent;

// Example usage
async function loadStory() {
    storyContent = await fetchStoryContent(storyTitle);
    // Further processing with storyContent
}

loadStory(); // Don't forget to call loadStory or the fetchStoryContent function with actual story title

