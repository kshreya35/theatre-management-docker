import { auth } from './firebase_config.js';

const addTheatreForm = document.getElementById("addTheatreForm");
const allTheatresDiv = document.getElementById("allTheatres");
const summaryDiv = document.getElementById("summary");

// Add Theatre
addTheatreForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const theatre = {
        name: document.getElementById("name").value,
        seats: Number(document.getElementById("seats").value),
        date: document.getElementById("date").value,
        timeSlot: document.getElementById("time").value, // <-- fixed
        price: Number(document.getElementById("price").value)
    };

    await fetch("/api/theatres", {
        method: "POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify(theatre)
    });

    addTheatreForm.reset(); // optional: clear form
    loadTheatres();          // reload theatre list
});

// Load Theatres
async function loadTheatres() {
    const res = await fetch("/api/theatres");
    const theatres = await res.json();
    allTheatresDiv.innerHTML = theatres.map(t => `
        <div class="theatre-card">
            <h3>${t.name}</h3>
            <p>Seats: ${t.seats} | Date: ${new Date(t.date).toLocaleDateString()} | Time: ${t.timeSlot} | Price: ${t.price}</p>
            <button onclick="deleteTheatre('${t._id}')">Delete</button>
        </div>
    `).join("");
    loadSummary();
}

// Delete Theatre
window.deleteTheatre = async (id) => {
    await fetch(`/api/theatres/${id}`, {method:"DELETE"});
    loadTheatres();
}

// Aggregation Summary
async function loadSummary() {
    const res = await fetch("/api/theatres/summary");
    const summary = await res.json();
    summaryDiv.innerHTML = summary.map(s => `<p>Date: ${new Date(s._id).toLocaleDateString()} | Booked: ${s.total}</p>`).join("");
}

loadTheatres();
