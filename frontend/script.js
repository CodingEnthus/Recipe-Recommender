// document.addEventListener("DOMContentLoaded",() =>{
// const fridge = document.querySelector(".fridge");
// const loginPanel = document.querySelector(".login-panel");

// /* open fridge when clicked */
// fridge.addEventListener("click", () => {
//     fridge.classList.toggle("open");
// });

// /* prevent closing when clicking inside login form */
// loginPanel.addEventListener("click", (event) => {
//     event.stopPropagation();
// });
// document.getElementById("loginBtn").addEventListener("click",async()=>{
//     const email=document.getElementById("email").value
//     const password=document.getElementById("password").value
//     const response=await fetch("http://127.0.0.1:8000/login",{
//         method:"POST",
//         headers:{
//             "Content-Type":"application/json"
//         },
//         body:JSON.stringify({
//             email:email,
//             password:password
//         })
//     })
//     const data=await response.json()
//     if(response.ok){
//         alert("Login Successfull")
//         console.log(data)
//         //later will be redirected to dashboard
//     }else{
//         alert(data.detail)
//     }
// })

// document.getElementById("signupBtn").addEventListener("click",async()=>{
//     const email=document.getElementById("email").value
//     const password=document.getElementById("password").value
//     const response=await fetch("http://127.0.0.1:8000/signup",{
//         method:"POST",
//         headers:{
//             "Content-Type":"application/json"
//         },
//         body:JSON.stringify({
//             email:email,
//             password:password
//         })
//     })
//     const data=await response.json()
//     if(response.ok){
//         alert("Account Created Successfully")
//     }else{
//         alert(data.detail)
//     }
// })
// })
document.addEventListener("DOMContentLoaded", () => {

const fridge = document.querySelector(".fridge");
const loginPanel = document.querySelector(".login-panel");

/* open fridge when clicked */
fridge.addEventListener("click", () => {
    fridge.classList.toggle("open");
});

/* prevent closing when clicking inside login form */
loginPanel.addEventListener("click", (event) => {
    event.stopPropagation();
});


/* LOGIN BUTTON */
document.getElementById("loginBtn").addEventListener("click", async () => {

    const email = document.getElementById("email").value
    const password = document.getElementById("password").value

    const response = await fetch("http://127.0.0.1:8000/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            email: email,
            password: password
        })
    })

    const data = await response.json()

    if (response.ok) {
        document.querySelector(".fridge").classList.add("open");

        setTimeout(()=>{
            window.location.href="dashboard.html"
        },1200);
        console.log(data)
    } else {
        alert(data.detail)
    }

})


/* SIGNUP BUTTON */
document.getElementById("signupBtn").addEventListener("click", async () => {

    const email = document.getElementById("email").value
    const password = document.getElementById("password").value

    const response = await fetch("http://127.0.0.1:8000/signup", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            email: email,
            password: password
        })
    })

    const data = await response.json()

    if (response.ok) {
        alert("Account Created Successfully 🎉")
    } else {
        alert(data.detail)
    }

})

})