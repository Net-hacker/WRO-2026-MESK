import iro from "https://cdn.jsdelivr.net/npm/@jaames/iro@5/+esm";
import noUiSlider from "https://cdn.jsdelivr.net/npm/nouislider@15.7.0/+esm";

// Stuff that happens at the begining of the programm
const container = document.getElementById("stream");
const slider = document.getElementById("slider");
const output = document.getElementById("output");
const tolerance = document.getElementById("toleranceR");
const toleranceOut = document.getElementById("toleranceV");
const angle = document.getElementById("angleSlider");
const angleOut = document.getElementById("angleDisplay");
var ColorPicker = new iro.ColorPicker("#picker", {
  width: 250,
  color: "rgb(255, 0, 0)",
  borderWidth: 1,
  borderColor: "#fff",
  layout: [
    {
      component: iro.ui.Slider,
      options: {
        sliderType: 'hue'
      }
    },
    {
      component: iro.ui.Slider,
      options: {
        sliderType: 'saturation'
      }
    },
    {
      component: iro.ui.Slider,
      options: {
        sliderType: 'value'
      }
    }
  ]
});
var ColorPicker2 = new iro.ColorPicker("#picker2", {
  width: 250,
  color: "rgb(255, 0, 0)",
  borderWidth: 1,
  borderColor: "#fff",
  layout: [
    {
      component: iro.ui.Slider,
      options: {
        sliderType: 'hue'
      }
    },
    {
      component: iro.ui.Slider,
      options: {
        sliderType: 'saturation'
      }
    },
    {
      component: iro.ui.Slider,
      options: {
        sliderType: 'value'
      }
    }
  ]
});

let Mask = 1;
let ignore_event = false;

ColorPicker.on('color:change', function(color) {
  if (ignore_event) return;
  const h = Math.round(color.hsv.h);
  const s = Math.round(color.hsv.s);
  const v = Math.round(color.hsv.v);
  output.textContent = `${h}, ${s}, ${v}`;
  const id = Mask;
  fetch("/set_value", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      ID: id,
      CID: "1",
      H: h,
      S: s,
      V: v
    })
  })
  .then(response => response.text())
  .then(response => {if (response != "done") console.log(response);})
});

ColorPicker2.on('color:change', function(color) {
  if (ignore_event) return;
  const h = Math.round(color.hsv.h);
  const s = Math.round(color.hsv.s);
  const v = Math.round(color.hsv.v);
  output.textContent = `${h}, ${s}, ${v}`;
  const id = Mask;
  fetch("/set_value", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      ID: id,
      CID: "2",
      H: h,
      S: s,
      V: v
    })
  })
  .then(response => response.text())
  .then(response => console.log(response))
});
UpdatePresets(1) //Add Preset Button to document
change_border(1) //Update slider values
UpdateTolerance(1) //Update Toleranzen
UpdateAngle() //Update Winkel

tolerance.oninput = function() {
  const id = Mask;
  const toleranceV = (tolerance.value * 0.0008).toFixed(6);
  toleranceOut.textContent = toleranceV;

  fetch("/send_tolerance", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      ID: id,
      TOLL: toleranceV
    })
  })
  .then(response => response.text())
  .then(response => console.log(response));
};

angle.oninput = function() {
  const id = Mask;
  const angleV = angle.value;
  angleOut.textContent = angleV

  fetch("/send_angle", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      ANG: angleV
    })
  })
  .then(response => response.text())
  .catch((e) => console.error(e));
};

//Functions

function change_border(id) {
  ignore_event = true;
  Mask = id;

  fetch(`/get_value?id=${id}`)
  .then(response => response.json())
  .then(data => {
    const lower = data.LOW;
    const upper = data.UP;

    ColorPicker.color.set({ h: lower[0], s: lower[1], v: lower[2] });
    ColorPicker2.color.set({ h: upper[0], s: upper[1], v: upper[2] });
    ignore_event = false;
  })
  .catch((e) => console.error(e));

  UpdatePresets(id);
}

function UpdateTolerance(id) {
  fetch(`/get_tolerance?id=${id}`)
  .then(response => response.json())
  .then(data => {
    const new_tolerance = data.TOLL;
    tolerance.value = new_tolerance / 0.0008;
  })
  .catch((e) => console.error(e));
}

function UpdateAngle() {
  fetch(`/get_angle`)
  .then(response => response.json())
  .then(data => {
    const new_angle = data.ANG;
    angle.value = new_angle / 360;
  })
  .catch((e) => console.error(e));
}

function UpdatePresets(id) {
  // Save Preset
  const presetDiv = document.getElementById("preset");
  if (!(presetDiv.hasChildNodes())) {

    // Save Preset Button
    var presetBtn = document.createElement("button");
    presetBtn.textContent = "Save Preset";
    presetBtn.id = id + "_presetBtn";
    presetBtn.addEventListener("click", function() { savePreset(id); });
    presetDiv.appendChild(presetBtn);
    // Load Preset Button
    var loadBtn = document.createElement("button");
    loadBtn.textContent = "Load Preset";
    loadBtn.id = id + "_loadBtn";
    loadBtn.addEventListener("click", function() { loadPreset(id); });
    presetDiv.appendChild(loadBtn);
  } else {
    // Delete old
    while (presetDiv.firstChild) {
      presetDiv.removeChild(presetDiv.firstChild);
    }
    // Save Preset Button
    var presetBtn = document.createElement("button");
    presetBtn.textContent = "Save Preset";
    presetBtn.id = id + "_presetBtn";
    presetBtn.addEventListener("click", function() { savePreset(id); });
    presetDiv.appendChild(presetBtn);
    // Load Preset Button
    var loadBtn = document.createElement("button");
    loadBtn.textContent = "Load Preset";
    loadBtn.id = id + "_loadBtn";
    loadBtn.addEventListener("click", function() { loadPreset(id); });
    presetDiv.appendChild(loadBtn);
  }
}

// Speichert das Preset via fetch / Flask
function savePreset(id) {
  fetch("/save", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      ID: id
    })
  })
  .then(response => {
    alert(`Preset ${id} saved!`)
  })
  .catch((e) => console.error(e));
}

// Lädt das Preset via fetch / Flask
function loadPreset(id) {
  fetch(`/load?id=${id}`)
  .then(response => {
    if (response.status == 404) {
      throw new Error("404 - Not found")
    }
    return response.json()
  })
  .then(data => {
    const lower = data.LOW;
    const upper = data.UP;

    ColorPicker.color.set({ h: upper[0], s: upper[1], v: upper[2] });
    ColorPicker2.color.set({ h: lower[0], s: lower[1], v: lower[2] });
  })
  .catch((e) => console.error(e));
}

// Zeigt die Maske (Result)
function showResult() {
  const existingR = document.getElementById("streamR");
  const existingL = document.getElementById("streamL");
  if (existingL) container.removeChild(existingL);
  if (existingR) { container.removeChild(existingR); return; }
  const streamR = document.createElement("img");
  streamR.id = "streamR";
  streamR.src = "/video_res";
  container.appendChild(streamR);
}

// Zeigt die Live Übertragung
function showLive() {
  const existingR = document.getElementById("streamR");
  const existingL = document.getElementById("streamL");
  if (existingR) container.removeChild(existingR);
  if (existingL) { container.removeChild(existingL); return; }
  const streamL = document.createElement("img");
  streamL.id = "streamL";
  streamL.src = "/video";
  container.appendChild(streamL);
}

// Für die onlick Events
document.getElementById("ResultB").addEventListener("click", showResult);
document.getElementById("LiveB").addEventListener("click", showLive);

const Motorslider = document.getElementById('motorSlider');
const display = document.getElementById('motorDisplay');
Motorslider.addEventListener('input', () => {
  display.textContent = Motorslider.value;
  fetch(`/set-motor?value=${Motorslider.value}`)
  .then(response => response.json())
  .then(data => {
    console.log(data);
  })
  .catch((e) => console.error(e));
});



window.change_border = change_border;
