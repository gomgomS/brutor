// Default language (English)

var currentLanguage = sessionStorage.getItem('currentLanguage');
console.log(currentLanguage == null);
if (currentLanguage == null){
    sessionStorage.setItem('currentLanguage', 'en');
}

// Function to fetch JSON data based on language
async function fetchLanguageData(lang) {
    console.log(lang)    
    let response = await fetch('../../static/assets/js/data_'+lang+'.json');
    if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
    }
    let data = await response.json();
    return data;
}

// Function to replace placeholders with language-specific content
async function updateContent(currentLanguage) {    
    const placeholders = document.querySelectorAll('[data-i18n]');    
    const data = await fetchLanguageData(currentLanguage);

    placeholders.forEach(element => {
        const key = element.getAttribute('data-i18n');
        console.log(data[key]);
        console.log("boomzz")
        if (data[key]) {
            element.textContent = data[key];
        }
    });
}

// Function to toggle language
async function toggleLanguage() {
    // Toggle current language
    var currentLanguage = sessionStorage.getItem('currentLanguage');    
    if (currentLanguage == "en" ) {  
        await updateContent(currentLanguage);      
        // alert("ubah current league jadi INDONESIA")
        sessionStorage.setItem('currentLanguage', 'id');
        
    } else {        
        await updateContent(currentLanguage)
        // alert("ubah current league jadi ENGLISH")
        sessionStorage.setItem('currentLanguage', 'en');       
    }

    // Update content after language switch
    await updateContent();
}

// Initial load: Fetch and display English content
document.addEventListener('DOMContentLoaded', async () => {
    var currentLanguage = sessionStorage.getItem('currentLanguage');
    await updateContent(currentLanguage);
});
