import { auth } from './firebase_config.js';

const searchForm = document.getElementById("searchForm");
const availableDiv = document.getElementById("availableTheatres");
const bookedDiv = document.getElementById("bookedTheatres");

// Search Filter
searchForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const query = {
        date: document.getElementById("filterDate").value,
        seats: Number(document.getElementById("seatNumber").value),
        condition: document.getElementById("seatCondition").value
    };
    const res = await fetch("/api/theatres/search", {
        method:"POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify(query)
    });
    const theatres = await res.json();
    renderAvailableTheatres(theatres);
});

// Render available theatres
function renderAvailableTheatres(theatres){
    availableDiv.innerHTML = theatres.map(t => `
        <div>
            <h3>${t.name}</h3>
            <p>Seats: ${t.seats} | Date: ${new Date(t.date).toLocaleDateString()} | Time: ${t.timeSlot} | Price: ${t.price}</p>
            <button ${t.bookedBy ? "disabled" : ""} onclick="bookTheatre('${t._id}')">Book</button>
        </div>
    `).join("");
}

// Book theatre
window.bookTheatre = async (id) => {
    const uid = auth.currentUser.uid;
    await fetch(`/api/theatres/book/${id}`, {
        method: "POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify({uid})
    });
    alert("Booked successfully!");
    loadBookedTheatres();
}

// Load booked theatres
async function loadBookedTheatres() {
    const uid = auth.currentUser.uid;
    const res = await fetch(`/api/theatres/booked/${uid}`);
    const theatres = await res.json();
    bookedDiv.innerHTML = theatres.map(t => `
        <div>
            <h3>${t.name}</h3>
            <p>Seats: ${t.seats} | Date: ${new Date(t.date).toLocaleDateString()} | Time: ${t.timeSlot} | Price: ${t.price}</p>
        </div>
    `).join("");
}

loadBookedTheatres();
