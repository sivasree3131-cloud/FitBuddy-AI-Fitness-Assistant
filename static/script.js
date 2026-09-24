const form = document.getElementById("fitnessForm");

const loading = document.getElementById("loading");
const errorBox = document.getElementById("errorBox");
const resultSection = document.getElementById("resultSection");
const generateButton = document.getElementById("generateButton");
const newPlanButton = document.getElementById("newPlanButton");


form.addEventListener("submit", async function (event) {

    event.preventDefault();

    errorBox.classList.add("hidden");
    resultSection.classList.add("hidden");
    loading.classList.remove("hidden");
    generateButton.disabled = true;


    const userData = {
        name: document.getElementById("name").value.trim(),
        age: Number(document.getElementById("age").value),
        weight: Number(document.getElementById("weight").value),
        goal: document.getElementById("goal").value,
        intensity: document.getElementById("intensity").value
    };


    try {

        const response = await fetch("/generate-workout", {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify(userData)
        });


        const data = await response.json();


        if (!response.ok) {

            throw new Error(
                data.detail
                    ? JSON.stringify(data.detail)
                    : "Unable to generate the plan."
            );

        }


        displayResults(userData, data);


    } catch (error) {

        console.error(error);

        errorBox.textContent =
            "Unable to generate your plan. Please check the server and try again.";

        errorBox.classList.remove("hidden");


    } finally {

        loading.classList.add("hidden");
        generateButton.disabled = false;

    }

});


function displayResults(userData, data) {

    // User information
    document.getElementById("resultName").textContent =
        userData.name;

    document.getElementById("resultAge").textContent =
        userData.age;

    document.getElementById("resultWeight").textContent =
        `${userData.weight} kg`;

    document.getElementById("resultGoal").textContent =
        userData.goal;

    document.getElementById("resultIntensity").textContent =
        userData.intensity;


    // Welcome message
    document.getElementById("welcomeText").textContent =
        `Hi ${userData.name}! Your personalized ${userData.goal.toLowerCase()} plan is ready.`;


    // Workout
    document.getElementById("workoutContent").innerHTML =
        formatAIText(
            data.plan_content || "Workout plan was not returned."
        );


    // Nutrition
    document.getElementById("nutritionContent").innerHTML =
        formatAIText(
            data.nutrition_tip || "Nutrition tips were not returned."
        );


    // Show result section
    resultSection.classList.remove("hidden");


    // Scroll to result
    setTimeout(() => {

        resultSection.scrollIntoView({
            behavior: "smooth",
            block: "start"
        });

    }, 100);

}


/*
    Convert Gemini's markdown-style response
    into a cleaner HTML display.
*/
function formatAIText(text) {

    let formatted = text;

    // Escape HTML
    formatted = formatted
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;");


    // Headings
    formatted = formatted.replace(
        /^### (.*)$/gm,
        '<h4 class="ai-heading">$1</h4>'
    );

    formatted = formatted.replace(
        /^## (.*)$/gm,
        '<h3 class="ai-heading">$1</h3>'
    );


    // Bold text
    formatted = formatted.replace(
        /\*\*(.*?)\*\*/g,
        '<strong>$1</strong>'
    );


    // Italic text
    formatted = formatted.replace(
        /\*(.*?)\*/g,
        '<em>$1</em>'
    );


    // Bullet points
    formatted = formatted.replace(
        /^\s*[\*\-]\s+(.*)$/gm,
        '<div class="ai-bullet">✓ $1</div>'
    );


    // Numbered list
    formatted = formatted.replace(
        /^\s*(\d+)\.\s+(.*)$/gm,
        '<div class="ai-number"><span>$1.</span> $2</div>'
    );


    // Horizontal lines
    formatted = formatted.replace(
        /^---$/gm,
        '<hr class="ai-divider">'
    );


    // Paragraph breaks
    formatted = formatted.replace(
        /\n{2,}/g,
        '<div class="ai-space"></div>'
    );


    // Single line breaks
    formatted = formatted.replace(
        /\n/g,
        "<br>"
    );


    return formatted;
}


newPlanButton.addEventListener("click", function () {

    resultSection.classList.add("hidden");

    form.reset();

    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });

});