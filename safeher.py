 
import re
import streamlit as st
import streamlit.components.v1 as components

# ---------------- PAGE SETTINGS ----------------
st.set_page_config(
    page_title="SafeHer",
    page_icon="🛡️",
    layout="wide"
)

# ---------------- DESIGN ----------------
st.markdown("""
<style>
.stApp {
    background: #07111f;
    color: white;
}
.title {
    font-size: 42px;
    font-weight: 800;
    color: white;
}
.subtitle {
    color: #9fb0c5;
    font-size: 17px;
}
.stButton button {
    background: #20e58a;
    color: #07111f;
    border-radius: 10px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ---------------- LOGIN ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:

    st.markdown(
        '<div class="title">🛡️ SafeHer</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">AI-powered real-time safety companion for women</div>',
        unsafe_allow_html=True
    )

    st.write("")
    st.subheader("Login")

    user_input = st.text_input(
        "Email or Phone Number",
        placeholder="Enter email or 10-digit mobile number"
    )

    if st.button("Login", use_container_width=True):

        value = user_input.strip()

        email_pattern = (
            r"^[A-Za-z0-9._%+-]+@"
            r"[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
        )

        phone_pattern = r"^[6-9][0-9]{9}$"

        valid_email = re.fullmatch(email_pattern, value)
        valid_phone = re.fullmatch(phone_pattern, value)

        if valid_email or valid_phone:
            st.session_state.logged_in = True
            st.session_state.username = value
            st.rerun()
        else:
            st.error(
                "Invalid input! Enter a valid email "
                "or 10-digit Indian mobile number."
            )

    st.stop()

# ---------------- DASHBOARD ----------------
st.markdown(
    '<div class="title">🛡️ SafeHer</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">AI-powered real-time safety companion for women</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns([4, 1])

with col1:
    st.caption("Logged in as: " + st.session_state.username)

with col2:
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

# ---------------- DASHBOARD HTML ----------------
html_code = r"""
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">

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
    gap: 15px;
}

.card {
    background: #101d2e;
    border: 1px solid #263b52;
    border-radius: 17px;
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
    font-size: 24px;
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

.sos {
    background: #e53935;
    color: white;
    width: 100%;
    padding: 20px;
    font-size: 21px;
}

.status {
    background: #0d2630;
    color: #20e58a;
    border-radius: 12px;
    padding: 15px;
    margin-top: 12px;
    overflow-wrap: anywhere;
}

a {
    color: #35a7ff;
}

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
        <div id="safety" class="value green">SAFE</div>
    </div>

    <div class="card">
        <div class="label">📍 LIVE GPS COORDINATES</div>
        <div id="coordinates" class="value green">
            Not detected
        </div>
    </div>

</div>

<div class="card">
    <div class="label">📍 CURRENT LOCATION</div>

    <div id="place" class="value green">
        Location not detected
    </div>

    <p id="address">
        Full address will appear here.
    </p>

    <button class="detect" onclick="startTracking()">
        📍 START LIVE GPS TRACKING
    </button>

    <div id="gpsStatus" class="status">
        Tap the button and allow location permission.
    </div>
</div>

<div class="card">
    <div class="label">🚔 NEARBY POLICE STATIONS</div>
    <div id="police">
        Start GPS tracking to find nearby police stations.
    </div>
</div>

<div class="card">
    <div class="label">🚨 EMERGENCY SOS</div>
    <p>In an emergency, use this button to call 112.</p>

    <button class="sos" onclick="sendSOS()">
        🚨 EMERGENCY SOS
    </button>
</div>

<p style="color:#9fb0c5;font-size:12px">
    SafeHer prototype | Map data by OpenStreetMap contributors.
</p>

<script>

// ---------------- LIVE TIME ----------------

function updateClock() {
    document.getElementById("clock").innerText =
        new Date().toLocaleTimeString();
}

setInterval(updateClock, 1000);
updateClock();


// ---------------- BATTERY ----------------

async function getBattery() {

    const batteryText =
        document.getElementById("battery");

    const chargingText =
        document.getElementById("charging");

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


// ---------------- GPS TRACKING ----------------

let watchId = null;
let lastAddressTime = 0;
let lastPoliceTime = 0;
let lastLat = null;
let lastLon = null;

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

            document.getElementById("coordinates").innerText =
                lat.toFixed(6) + ", " + lon.toFixed(6);

            document.getElementById("gpsStatus").innerText =
                "🟢 Live GPS tracking active | Accuracy: " +
                Math.round(position.coords.accuracy) + " metres";

            const moved = lastLat === null ||
                distanceMeters(lastLat, lastLon, lat, lon) > 100;

            const now = Date.now();

            if (moved || now - lastAddressTime > 30000) {
                lastLat = lat;
                lastLon = lon;
                lastAddressTime = now;
                getAddress(lat, lon);
            }

            if (moved || now - lastPoliceTime > 120000) {
                lastPoliceTime = now;
                findPolice(lat, lon);
            }
        },

        function(error) {

            const messages = {
                1: "Location permission denied. Allow location in Chrome.",
                2: "GPS position unavailable. Check phone location settings.",
                3: "GPS request timed out. Please try again."
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


// ---------------- LOCATION NAME AND ADDRESS ----------------

async function getAddress(lat, lon) {

    const place = document.getElementById("place");
    const address = document.getElementById("address");

    try {

        const url =
            "https://nominatim.openstreetmap.org/reverse" +
            "?format=jsonv2&lat=" + lat +
            "&lon=" + lon;

        const response = await fetch(url);

        if (!response.ok) throw new Error("Address service unavailable");

        const data = await response.json();
        const a = data.address || {};

        const city =
            a.city || a.town || a.village ||
            a.suburb || a.county || "Unknown area";

        const state = a.state || "";

        place.innerText = city + ", " + state;

        address.innerText =
            data.display_name || "Full address unavailable.";

    } catch(error) {

        place.innerText = "Location name unavailable";
        address.innerText =
            "Could not load address. GPS coordinates are still available.";

    }
}


// ---------------- NEARBY POLICE STATIONS ----------------

async function findPolice(lat, lon) {

    const output = document.getElementById("police");

    output.innerText = "Searching within 5 km...";

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
                method: "POST",
                body: "data=" + encodeURIComponent(query)
            }
        );

        if (!response.ok) throw new Error("Police data unavailable");

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

            const item = document.createElement("p");
            item.innerText = "🚔 " + name;

            output.appendChild(item);
        });

    } catch(error) {

        output.innerText =
            "Police station data unavailable. Try again later.";

    }
}


// ---------------- EMERGENCY SOS ----------------

function sendSOS() {

    document.getElementById("safety").innerText =
        "SOS ACTIVE";

    document.getElementById("safety").style.color =
        "#ff4d4d";

    document.getElementById("gpsStatus").innerText =
        "Emergency call option opened.";

    window.location.href = "tel:112";
}

</script>

</body>
</html>
"""

components.html(
    html_code,
    height=1250,
    scrolling=True
)

st.caption(
    "SafeHer prototype | GPS and battery features depend on "
    "device, browser permissions and network availability."
)
