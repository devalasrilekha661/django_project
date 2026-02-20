function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

let login_btn = document.getElementById("login_btn");

login_btn.addEventListener("click", (e) => {
    e.preventDefault();

    let email = document.getElementById("email").value;
    let password = document.getElementById("password").value;
    let role = document.getElementById("role").value;

    let login_p_d = {
        e: email,
        p: password,
        r: role
    };

    console.log(login_p_d);

    fetch("http://127.0.0.1:8000/login_validation/", {
    method: "POST",
    headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrftoken")
    },
    body: JSON.stringify(login_p_d)
})
.then(response => response.json())   // 🔥 IMPORTANT
.then(data => {

    console.log("Backend Response:", data); // Debug

    if (data.id && data.r_url) {
        window.location.href = `/${data.r_url}/${data.id}/`;
    } else {
        alert(data.msg);
    }
})
.catch(error => {
    console.log("Error:", error);
});

}) 
