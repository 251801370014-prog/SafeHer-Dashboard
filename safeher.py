
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="SafeHer",
    page_icon="🛡️",
    layout="wide"
)

# ---------------- LOGIN ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.markdown("""
    <style>
    .stApp {
        background: #07111f;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

    st.title("🛡️ SafeHer")
    st.subheader("Women's Safety Dashboard")
    st.write("Welcome! Please enter your username.")

    username = st.text_input("Enter Username")

    if st.button("Login", use_container_width=True):
        if username.strip():
            st.session_state.logged_in = True
            st.session_state.username = username.strip()
            st.rerun()
        else:
            st.warning("Please enter your username.")

    st.stop()

# ---------------- DASHBOARD ----------------
col1, col2 = st.columns([5, 1])

with col1:
    st.title("🛡️ SafeHer Dashboard")
    st.caption("Welcome, " + st.session_state.username)

with col2:
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

html_code = r"""
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body {
    background:#07111f;
    color:white;
    font-family:Arial,sans-serif;
    margin:0;
}
.card {
    background:#101d2e;
    border:1px solid #263b52;
    border-radius:15px;
    padding:20px;
    margin:10px 0;
}
.grid {
    display:grid;
    grid-template-columns:repeat(2,1fr);
    gap:12px;
}
h2 { color:#20e58a; }
.value {
    font-size:18px;
    margin-top:12px;
    overflow-wrap:anywhere;
}
button {
    border:0;
    border-radius:10px;
    padding:13px;
    font-size:15px;
    font-weight:bold;
    cursor:pointer;
}
.green {background:#20e58a;color:#07111f;}
.red {
    background:#e53935;
    color:white;
    width:100%;
    font-size:19px;
    padding:18px;
}
.blue {background:#35a7ff;color:#07111f;}
small {color:#9eb1c7;}
</style>
</head>

<body>

<div class="grid">

<div class="card">
<h2>🔋 Battery Status</h2>
<div class="value" id="battery">Checking...</div>
</div>

<div class="card">
<h2>🕒 Live Time</h2>
<div class="value" id="clock">--</div>
</div>

<div class="card">
<h2>🛡️ Safety Status</h2>
<div class="value" style="color:#20e58a">
● SAFE
</div>
</div>

<div class="card">
<h2>📍 Live Coordinates</h2>
<div class="value" id="coordinates">Not detected</div>
</div>

</div>

<div class="card">
<h2>📍 Current Location</h2>
<div class="value" id="place">Tap the button to detect location</div>
<br>
<div id="address">Full address will appear here.</div>
<br>
<button class="green" onclick="getLocation()">
Detect My Location
</button>
</div>

<div class="card">
<h2>🚔 Nearby Police Stations</h2>
<div id="police">Detect your location first.</div>
</div>

<div class="card">
<h2>🚨 Emergency SOS</h2>
<p>In an emergency, use this button to call 112.</p>
<button class="red" onclick="callSOS()">
🚨 EMERGENCY SOS
</button>
</div>

<p><small>
Location data: OpenStreetMap contributors.
Location is requested only after you tap Detect My Location.
</small></p>

<script>
setInterval(() => {
 document.getElementById("clock").innerText =
 new Date().toLocaleString();
}, 1000);

if (navigator.getBattery) {
 navigator.getBattery().then(b => {
  function updateBattery() {
   document.getElementById("battery").innerText =
   Math.round(b.level * 100) + "%";
  }
  updateBattery();
  b.addEventListener("levelchange", updateBattery);
 }).catch(() => {
  document.getElementById("battery").innerText =
  "Not available";
 });
} else {
 document.getElementById("battery").innerText =
 "Not supported";
}

function getLocation() {
 const place = document.getElementById("place");
 place.innerText = "Requesting GPS permission...";
 document.getElementById("police").innerText = "Loading...";

 if (!navigator.geolocation) {
  place.innerText = "Geolocation not supported.";
  return;
 }

 navigator.geolocation.getCurrentPosition(
  async function(position) {
   const lat = position.coords.latitude;
   const lon = position.coords.longitude;

   document.getElementById("coordinates").innerText =
    lat.toFixed(6) + ", " + lon.toFixed(6);

   place.innerText = "Finding location name...";
   document.getElementById("address").innerText =
    "Loading address...";

   try {
    const url =
     `https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat=${lat}&lon=${lon}`;

    const response = await fetch(url);
    const data = await response.json();

    const a = data.address || {};
    const city = a.city || a.town || a.village ||
                 a.suburb || a.county || "Unknown area";
    const state = a.state || "";
    place.innerText = city + ", " + state;
    document.getElementById("address").innerText =
     data.display_name || "Address not available.";
   } catch(error) {
    place.innerText = "Location name unavailable.";
    document.getElementById("address").innerText =
     "Please try again later.";
   }

   findPolice(lat, lon);
  },

  function(error) {
   place.innerText =
    "Location permission denied or GPS unavailable.";
   document.getElementById("police").innerText =
    "Location needed to find nearby police stations.";
  },
  {enableHighAccuracy:true, timeout:20000}
 );
}

async function findPolice(lat, lon) {
 const output = document.getElementById("police");
 output.innerText = "Searching nearby police stations...";

 const query = `
 [out:json][timeout:20];
 (
  node["amenity"="police"](around:5000,${lat},${lon});
  way["amenity"="police"](around:5000,${lat},${lon});
  relation["amenity"="police"](around:5000,${lat},${lon});
 );
 out center tags;
 `;

 try {
  const response = await fetch(
   "https://overpass-api.de/api/interpreter",
   {
    method:"POST",
    body:"data=" + encodeURIComponent(query)
   }
  );

  const data = await response.json();

  if (!data.elements || data.elements.length === 0) {
   output.innerText =
    "No mapped police stations found within 5 km.";
   return;
  }

  output.innerHTML = "";

  data.elements.slice(0,10).forEach((station) => {
   const name = station.tags.name || "Police Station";
   const item = document.createElement("p");
   item.textContent = "🚔 " + name;
   output.appendChild(item);
  });

 } catch(error) {
  output.innerText =
   "Could not load police station data. Try again later.";
 }
}

function callSOS() {
 window.location.href = "tel:112";
}
</script>
</body>
</html>
"""

components.html(html_code, height=1050, scrolling=True)
