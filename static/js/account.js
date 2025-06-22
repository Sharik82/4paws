function displayGreeting() {
    const greetingElement = document.getElementById('greeting');
    const currentHour = new Date().getHours();

    if (currentHour >= 6 && currentHour < 12) {
        greetingElement.textContent = 'Доброго ранку!';
    } else if (currentHour >= 12 && currentHour < 18) {
        greetingElement.textContent = 'Доброго дня!';
    } else if (currentHour >= 18 && currentHour < 24) {
        greetingElement.textContent = 'Доброго вечора!';
    } else {
        greetingElement.textContent = 'Доброї ночі!';
    }
}


window.onload = function() {
    displayGreeting();
};

const settingsLink = document.getElementById('settings-link');
const settingsPanel = document.getElementById('settings-panel');


function openSettingsPanel() {
    
    if (settingsPanel.classList.contains('visible')) {
        settingsPanel.classList.remove('visible');
        settingsPanel.classList.add('hidden');
    } else {
        
        settingsPanel.classList.remove('hidden');
        settingsPanel.classList.add('visible');
    }
}

settingsLink.addEventListener('click', function(event) {
    event.preventDefault(); 
    openSettingsPanel();    
});
