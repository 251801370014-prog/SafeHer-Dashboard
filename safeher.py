 
 
import re
import streamlit as st
import streamlit.components.v1 as components

# PAGE SETTINGS
st.set_page_config(
    page_title="SafeHer",
    page_icon="🛡️",
    layout="wide"
)

# LOGIN SYSTEM
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
    st.caption("AI-powered real-time safety companion for women")
    st.subheader("Login")

    user_input = st.text_input(
        "Email or Phone Number",
        placeholder="Enter email or 10-digit mobile number"
    )

    if st.button("Login", use_container_width=True):
        value = user_input.strip()

        email_valid = re.fullmatch(
            r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
            value
        )

        phone_valid = re.fullmatch(
            r"[6-9][0-9]{9}",
            value
        )

        if email_valid or phone_valid:
            st.session_state.logged_in = True
            st.session_state.username = value
            st.rerun()
        else:
            st.error("Enter a valid email or 10-digit Indian mobile number.")

    st.stop()

# DASHBOARD HEADER
st.markdown("""
<style>
.stApp {
    background: #07111f;
    color: white;
}
</style>
""", unsafe_allow_html=True)

col1, col2 = st.columns([4, 1])

with col1:
    st.title("🛡️ SafeHer")
    st.caption("AI-powered real-time safety companion for women")
    st.caption("Logged in as: " + st.session_state.username)

with col2:
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

# DASHBOARD HTML
html_code = r"""
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">

<link rel="stylesheet"
href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">

<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>

<style>
body {
    margin: 0;
    background: #07111f;
    color: white;
    font-family: Arial, sans-serif;
}

.dashboard {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 14px;
}

.card {
    background: #101d2e;
    border: 1px solid #263b52;
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 14px;
    box-sizing: border-box;
}

.label {
    color: #9fb0c5;
    font-size: 15px;
    margin-bottom: 12px;
}

.value {
    font-size: 23px;
    font-weight: bold;
    overflow-wrap: anywhere;
}

.green { color: #20e58a; }
.blue { color: #35a7ff; }

button {
    border: none;
    border-radius: 10px;
    padding: 14px;
    font-size: 16px;
    font-weight: bold;
    cursor: pointer;
}

.detect {
    background: #20e58a;
    color: #07111f;
    width: 100%;
}

.stop {
    background: #64748b;
    color: white;
    width: 100%;
    margin-top: 10px;
}

.sos {
    background: #e53935;
    color: white;
    width: 100%;
    padding: 20px;
    font-size: 20px;
}

.status {
    background: #0d2630;
    color: #20e58a;
    padding: 14px;
    border-radius: 10px;
    margin-top: 12px;
    overflow-wrap: anywhere;
}

#liveMap {
    height: 350px;
    width: 100%;
    border-radius: 12px;
    background: #182b3e;
    z-index: 1;
}

.police-item {
    border-bottom: 1px solid #263b52;
    padding: 10px 0;
}

small { color: #9fb0c5; }

@media(max-width: 650px) {
    .dashboard {
        grid-template-columns: 1fr;
    }
}
</style>
</head>

<body>

<div class="dashboard">

    <div class="card">
        <div class="label">🔋 BATTERY STATUS</div>
        <div id="battery" class="value blue">Checking...</div>
        <div id="charging">Checking...</div>
    </div>

    <div class="card">
        <div class="label">🕒 LIVE TIME</div>
        <div id="clock" class="value">--:--:--</div>
    </div>

    <div class="card">
        <div class="label">🛡️ SAFETY STATUS</div>
        <div id="safety" class="value green">● SAFE</div>
    </div>

    <div class="card">
        <div class="label">📍 LIVE GPS COORDINATES</div>
        <div id="coordinates" class="value green">Not detected</div>
    </div>

</div>

<div class="card">
    <div class="label">🗺️ LIVE GPS MAP</div>
    <div id="liveMap"></div>
    <p id="mapStatus">Start GPS tracking to show your location on map.</p>
</div>

<div class="card">
    <div class="label">📍 CURRENT LOCATION</div>
    <div id="place" class="value green">Location not detected</div>
    <p id="address">Full address will appear here.</p>

    <button class="detect" onclick="startTracking()">
        📍 START LIVE GPS TRACKING
    </button>

    <button class="stop" onclick="stopTracking()">
        STOP TRACKING
    </button>

    <div id="gpsStatus" class="status">
        Allow location permission to start tracking.
    </div>
</div>

<div class="card">
    <div class="label">🚔 NEARBY POLICE STATIONS</div>
    <div id="police">Start GPS tracking to find nearby stations.</div>
</div>

<div class="card">
    <div class="label">🚨 EMERGENCY SOS</div>
    <p>In an emergency, use this button to call 112.</p>
    <button class="sos" onclick="sendSOS()">
        🚨 EMERGENCY SOS
    </button>
</div>

<p><small>
SafeHer prototype | Map data © OpenStreetMap contributors.
</small></p>

<script>

// LIVE CLOCK
function updateClock() {
    document.getElementById("clock").innerText =
        new Date().toLocaleTimeString();
}
setInterval(updateClock, 1000);
updateClock();


// BATTERY STATUS
async function getBattery() {
    const batteryText = document.getElementById("battery");
    const chargingText = document.getElementById("charging");

    if (!navigator.getBattery) {
        batteryText.innerText = "Not supported";
        chargingText.innerText = "";
        return;
    }

    try {
        const battery = await navigator.getBattery();

        function update() {
            batteryText.innerText =
                Math.round(battery.level * 100) + "%";

            chargingText.innerText =
                battery.charging ? "⚡ Charging" : "🔋 Not charging";
        }

        update();
        battery.addEventListener("levelchange", update);
        battery.addEventListener("chargingchange", update);

    } catch(error) {
        batteryText.innerText = "Unavailable";
    }
}
getBattery();


// MAP INITIALIZATION
let map = null;
let marker = null;
let routeLine = null;
let watchId = null;
let lastLat = null;
let lastLon = null;
let lastAddressTime = 0;
let lastPoliceTime = 0;

function initializeMap() {
    if (map || !window.L) return;

    map = L.map("liveMap").setView([17.0, 83.0], 6);

    L.tileLayer(
        "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
        {
            attribution: "&copy; OpenStreetMap contributors",
            maxZoom: 19
        }
    ).addTo(map);

    routeLine = L.polyline([], {
        color: "#20e58a",
        weight: 4
    }).addTo(map);
}

initializeMap();


// UPDATE LIVE MAP MARKER
function updateLiveMap(lat, lon) {
    initializeMap();

    if (!map) {
        document.getElementById("mapStatus").innerText =
            "Map library could not load. Check internet connection.";
        return;
    }

    const position = [lat, lon];

    if (!marker) {
        marker = L.marker(position).addTo(map);
        marker.bindPopup("Your current location");
    } else {
        marker.setLatLng(position);
    }

    routeLine.addLatLng(position);
    map.setView(position, 16);

    document.getElementById("mapStatus").innerText =
        "🟢 Your live location is displayed on the map.";
}


// DISTANCE CALCULATION
function distanceMeters(lat1, lon1, lat2, lon2) {
    const R = 6371000;
    const rad = x => x * Math.PI / 180;

    const dLat = rad(lat2 - lat1);
    const dLon = rad(lon2 - lon1);

    const a =
        Math.sin(dLat / 2) ** 2 +
        Math.cos(rad(lat1)) *
        Math.cos(rad(lat2)) *
        Math.sin(dLon / 2) ** 2;

    return R * 2 * Math.atan2(
        Math.sqrt(a),
        Math.sqrt(1 - a)
    );
}


// START CONTINUOUS GPS
function startTracking() {

    if (!navigator.geolocation) {
        document.getElementById("gpsStatus").innerText =
            "GPS is not supported by this browser.";
        return;
    }

    if (watchId !== null) {
        navigator.geolocation.clearWatch(watchId);
    }

    document.getElementById("gpsStatus").innerText =
        "Requesting GPS permission...";

    watchId = navigator.geolocation.watchPosition(

        function(position) {

            const lat = position.coords.latitude;
            const lon = position.coords.longitude;
            const now = Date.now();

            document.getElementById("coordinates").innerText =
                lat.toFixed(6) + ", " + lon.toFixed(6);

            document.getElementById("gpsStatus").innerText =
                "🟢 Live GPS tracking active | Accuracy: " +
                Math.round(position.coords.accuracy) + " metres";

            updateLiveMap(lat, lon);

            const moved = lastLat === null ||
                distanceMeters(lastLat, lastLon, lat, lon) > 100;

            if (moved || now - lastAddressTime > 30000) {
                lastAddressTime = now;
                getAddress(lat, lon);
            }

            if (moved || now - lastPoliceTime > 120000) {
                lastPoliceTime = now;
                findPolice(lat, lon);
            }

            lastLat = lat;
            lastLon = lon;
        },

        function(error) {

            const messages = {
                1: "Location permission denied. Allow location in Chrome.",
                2: "GPS unavailable. Check phone location settings.",
                3: "GPS timed out. Please try again."
            };

            document.getElementById("gpsStatus").innerText =
                messages[error.code] || "GPS error occurred.";
        },

        {
            enableHighAccuracy: true,
            maximumAge: 3000,
            timeout: 20000
        }
    );
}


// STOP GPS
function stopTracking() {
    if (watchId !== null) {
        navigator.geolocation.clearWatch(watchId);
        watchId = null;
    }

    document.getElementById("gpsStatus").innerText =
        "GPS tracking stopped.";
    document.getElementById("mapStatus").innerText =
        "Tracking stopped.";
}


// REVERSE GEOCODING - LOCATION NAME AND ADDRESS
async function getAddress(lat, lon) {

    const place = document.getElementById("place");
    const address = document.getElementById("address");

    try {
        const url =
            "https://nominatim.openstreetmap.org/reverse" +
            "?format=jsonv2&lat=" + lat + "&lon=" + lon;

        const response = await fetch(url);

        if (!response.ok) throw new Error("Address unavailable");

        const data = await response.json();
        const a = data.address || {};

        const city =
            a.city || a.town || a.village ||
            a.suburb || a.county || "Unknown area";

        place.innerText =
            city + ", " + (a.state || "");

        address.innerText =
            data.display_name || "Full address unavailable.";

    } catch(error) {
        place.innerText = "Location name unavailable";
        address.innerText =
            "Address service unavailable. GPS coordinates are available.";
    }
}


// NEARBY POLICE STATIONS
async function findPolice(lat, lon) {

    const output = document.getElementById("police");
    output.innerText = "Searching within 5 km...";

    const query = `
    [out:json][timeout:25];
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
                method: "POST",
                body: "data=" + encodeURIComponent(query)
            }
        );

        if (!response.ok) throw new Error("Service unavailable");

        const data = await response.json();
        output.innerHTML = "";

        if (!data.elements || data.elements.length === 0) {
            output.innerText =
                "No mapped police stations found within 5 km.";
            return;
        }

        data.elements.slice(0, 10).forEach(station => {

            const name =
                station.tags.name || "Police Station";

            const item = document.createElement("div");
            item.className = "police-item";
            item.textContent = "🚔 " + name;

            output.appendChild(item);
        });

    } catch(error) {
        output.innerText =
            "Police station data unavailable. Try again later.";
    }
}


// EMERGENCY SOS
function sendSOS() {
    document.getElementById("safety").innerText =
        "SOS CALL REQUESTED";

    document.getElementById("safety").style.color =
        "#ff4d4d";

    window.location.href = "tel:112";
}

</script>

</body>
</html>
"""

# RENDER DASHBOARD
components.html(
    html_code,
    height=1550,
    scrolling=True
)

st.caption(
    "SafeHer prototype | GPS works while the dashboard is active "
    "and browser location permission is allowed."
)
