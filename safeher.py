import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="SafeHer",
    page_icon="🛡️",
    layout="wide"
)

st.markdown("""
<style>
    .stApp {
        background: #07111f;
        color: white;
    }

    .title {
        font-size: 42px;
        font-weight: 800;
        margin-bottom: 5px;
    }

    .subtitle {
        color: #9fb0c5;
        font-size: 17px;
        margin-bottom: 25px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="title">🛡️ SafeHer</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">AI-powered real-time safety companion for women</div>',
    unsafe_allow_html=True
)

# Real-time dashboard
components.html("""
<!DOCTYPE html>
<html>
<head>
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
    gap: 18px;
}

.card {
    background: #101d2e;
    border: 1px solid #263b52;
    border-radius: 18px;
    padding: 22px;
    min-height: 130px;
    box-sizing: border-box;
}

.label {
    color: #8fa4ba;
    font-size: 14px;
    margin-bottom: 12px;
}

.value {
    font-size: 28px;
    font-weight: bold;
}

.green {
    color: #20e58a;
}

.blue {
    color: #35a7ff;
}

.orange {
    color: #ffb84d;
}

.sos {
    background: #e53935;
    color: white;
    border: none;
    border-radius: 15px;
    width: 100%;
    padding: 20px;
    font-size: 22px;
    font-weight: bold;
    margin-top: 18px;
}

.sos:active {
    transform: scale(0.98);
}

.status {
    margin-top: 20px;
    padding: 15px;
    background: #0d2630;
    border-radius: 12px;
    color: #20e58a;
}

@media(max-width:700px) {
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
        <div id="charging" class="green">Checking charging...</div>
    </div>

    <div class="card">
        <div class="label">📍 LIVE LOCATION</div>
        <div id="location" class="value green">Requesting GPS...</div>
    </div>

    <div class="card">
        <div class="label">🛡️ SAFETY STATUS</div>
        <div id="safety" class="value green">SAFE</div>
    </div>

    <div class="card">
        <div class="label">🕐 LIVE TIME</div>
        <div id="time" class="value">--:--:--</div>
    </div>

</div>

<button class="sos" onclick="sendSOS()">
🚨 EMERGENCY SOS
</button>

<div id="message" class="status">
System monitoring active...
</div>

<script>


// ---------------- LIVE TIME ----------------

function updateTime() {
    let now = new Date();
    document.getElementById("time").innerText =
        now.toLocaleTimeString();
}

setInterval(updateTime, 1000);
updateTime();


// ---------------- BATTERY ----------------

async function getBattery() {

    if (!navigator.getBattery) {
        document.getElementById("battery").innerText =
            "Not supported";
        document.getElementById("charging").innerText =
            "Battery API unavailable";
        return;
    }

    try {

        const battery = await navigator.getBattery();

        function updateBattery() {

            let level = Math.round(battery.level * 100);

            document.getElementById("battery").innerText =
                level + "%";

            if (battery.charging) {
                document.getElementById("charging").innerText =
                    "⚡ Charging";
            } else {
                document.getElementById("charging").innerText =
                    "🔋 Not charging";
            }

        }

        updateBattery();

        battery.addEventListener(
            "levelchange",
            updateBattery
        );

        battery.addEventListener(
            "chargingchange",
            updateBattery
        );

    } catch(e) {

        document.getElementById("battery").innerText =
            "Unavailable";

    }
}

getBattery();


// ---------------- GPS LOCATION ----------------

function startLocation() {

    if (!navigator.geolocation) {

        document.getElementById("location").innerText =
            "GPS unavailable";

        return;
    }

    navigator.geolocation.watchPosition(

        function(position) {

            let lat = position.coords.latitude;
            let lon = position.coords.longitude;

            document.getElementById("location").innerHTML =
                lat.toFixed(5) +
                "<br>" +
                lon.toFixed(5);

            document.getElementById("message").innerText =
                "📍 Live GPS location updated";

        },

        function(error) {

            document.getElementById("location").innerText =
                "Permission required";

            document.getElementById("message").innerText =
                "Please allow location permission";

        },

        {
            enableHighAccuracy: true,
            maximumAge: 5000,
            timeout: 10000
        }
    );
}

startLocation();


// ---------------- SOS ----------------

function sendSOS() {

    document.getElementById("safety").innerText =
        "SOS ACTIVE";

    document.getElementById("safety").style.color =
        "#ff4d4d";

    document.getElementById("message").innerText =
        "🚨 Emergency mode activated";

    // Replace with your emergency contact number
    window.location.href = "tel:112";
}

</script>

</body>
</html>
""", height=650)

st.markdown("---")

st.caption(
    "SafeHer prototype • GPS and battery information depends on browser/device permissions and support."
)
