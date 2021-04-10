function updateHighlights() {
    const prereqElements = document.getElementsByClassName("classpreqs");
    
    courses_stack.forEach(e => {
        for(let i = 0; i < prereqElements.length; i++) {
            const element = prereqElements[i];
            element.innerHTML = element.innerHTML.replaceAll(e, `<span class="highlighted">${e}</span>`);
        }
    });
}