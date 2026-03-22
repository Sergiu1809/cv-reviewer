const submitBtn = document.getElementById("submit-btn")
const cvText = document.getElementById("cv-text")
const cvFeedback = document.getElementById("cv-feedback")

async function getAPIResponse(){
    const apiUrl = "http://localhost:8000/review";

    const response = await fetch(apiUrl, {
        method:"POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({resume_text: cvText.value})
    })

    if(!response.ok){
        throw new Error("Could not fetch data")
    }

    return await response.json()
}

async function displayFeedback(){
    cvFeedback.textContent = "Analyzing your CV..."
    
    try{
    const data = await getAPIResponse();
    cvFeedback.innerHTML = marked.parse(data.response)
    }
    catch(error){
        cvFeedback.textContent = "Something went wrong. Please try again.";
    }
}

submitBtn.addEventListener("click", () =>{
   displayFeedback()
})