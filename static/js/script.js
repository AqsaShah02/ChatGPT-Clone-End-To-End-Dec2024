async function postData(url = "", data = {}) {
    try {
        const response = await fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(data),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        return response.json();
    } catch (error) {
        console.error("Error with fetch:", error);
    }
}

sendButton.addEventListener("click",async ()  => {
   
    questionInput = document.getElementById("questionInput").value;
   document.getElementById("questionInput").value = "";
    document.querySelector(".right2").style.display = "block"
    document.querySelector(".right-1").style.display = "none"

    question.innerHTML = questionInput;
    
    // get the answer and populate it

    let result = await postData("/api" , {"question" : questionInput})
    solution.innerHTML = result.result
});


sendButton1.addEventListener("click",async ()  => {
   
    questionInput = document.getElementById("questionInput").value;
   document.getElementById("questionInput").value = "";
    document.querySelector(".right2").style.display = "block"
    document.querySelector(".right-1").style.display = "none"

    question.innerHTML = questionInput;
    
    // get the answer and populate it

    let result = await postData("/api" , {"question" : questionInput})
    solution.innerHTML = result.result
});