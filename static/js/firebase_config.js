import { initializeApp } from "https://www.gstatic.com/firebasejs/10.6.0/firebase-app.js";
import { getAuth } from "https://www.gstatic.com/firebasejs/10.6.0/firebase-auth.js";
import { getFirestore } from "https://www.gstatic.com/firebasejs/10.6.0/firebase-firestore.js";

const firebaseConfig = {
  apiKey: "AIzaSyDvEzevp6chaMIgl6lfAMHbj3BrkDUN5GY",
  authDomain: "practical9-ede02.firebaseapp.com",
  projectId: "practical9-ede02",
  storageBucket: "practical9-ede02.firebasestorage.app",
  messagingSenderId: "497503249122",
  appId: "1:497503249122:web:f48f7bdf89d7a123bb74bb",
  measurementId: "G-P2F86L4QXQ"
};

const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);
export const db = getFirestore(app);
