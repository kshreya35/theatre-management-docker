import { auth } from './firebase_config.js';
import { createUserWithEmailAndPassword, signInWithEmailAndPassword } from "https://www.gstatic.com/firebasejs/10.6.0/firebase-auth.js";

// ------------------- REGISTER -------------------
const registerForm = document.getElementById("registerForm");
if (registerForm) {
    registerForm.addEventListener("submit", (e) => {
        e.preventDefault();
        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;
        const role = document.getElementById("role").value;

        createUserWithEmailAndPassword(auth, email, password)
        .then(userCredential => {
            const uid = userCredential.user.uid;
            // Save user to MongoDB
            fetch("/api/users", {
                method: "POST",
                headers: {"Content-Type":"application/json"},
                body: JSON.stringify({uid, email, role})
            }).then(res => res.json())
              .then(() => window.location = "/login"); // <-- use Flask route
        }).catch(err => alert(err.message));
    });
}

// ------------------- LOGIN -------------------
const loginForm = document.getElementById("loginForm");
if (loginForm) {
    loginForm.addEventListener("submit", (e) => {
        e.preventDefault();
        const email = document.getElementById("loginEmail").value;
        const password = document.getElementById("loginPassword").value;

        signInWithEmailAndPassword(auth, email, password)
.then(userCredential => {
    const uid = userCredential.user.uid;
    // Fetch only the logged-in user
    fetch(`/api/users/${uid}`)
    .then(res => res.json())
    .then(user => {
        if(user.role === "admin") window.location = "/admin";
        else window.location = "/producer";
    });
}).catch(err => alert(err.message));

    });
}
