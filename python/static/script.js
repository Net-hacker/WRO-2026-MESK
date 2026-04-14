import iro from "https://cdn.jsdelivr.net/npm/@jaames/iro@5/+esm";
import noUiSlider from "https://cdn.jsdelivr.net/npm/nouislider@15.7.0/+esm";

// Hier alles mit Colorpicker
const container = document.getElementById("stream");
const slider = document.getElementById("slider");
const output = document.getElementById("output");
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
  const border = Mask + "1";
  fetch(`/set_value?value=${h}, ${s}, ${v}&id=${border}`)
    .then(response => response.text())
    .then(response => console.log(response))
});

ColorPicker2.on('color:change', function(color) {
  if (ignore_event) return;
  const h = Math.round(color.hsv.h);
  const s = Math.round(color.hsv.s);
  const v = Math.round(color.hsv.v);
  output.textContent = `${h}, ${s}, ${v}`;
  const border = Mask + "2";
  fetch(`/set_value?value=${h}, ${s}, ${v}&id=${border}`)
    .then(response => response.text())
    .then(response => console.log(response))
});

function change_border(id) {
  ignore_event = true;
  Mask = id;
  let colors;
  fetch(`/get_value?id=${id + "1"}`)
    .then(response => response.text())
      .then(response => {
      console.log(response);
      colors = response.split(",").map(Number);
      console.log(colors);
      ColorPicker.color.set({ h: colors[0], s: colors[1], v: colors[2] });
      const h = Math.round(ColorPicker.color.hsv.h);
      const s = Math.round(ColorPicker.color.hsv.s);
      const v = Math.round(ColorPicker.color.hsv.v);
      output.textContent = `${h}, ${s}, ${v}`;
      console.log("Border geändert")
    }
  )
  fetch(`/get_value?id=${id + "2"}`)
    .then(response => response.text())
      .then(response => {
      console.log(response);
      colors = response.split(",").map(Number);
      console.log(colors);
      ColorPicker2.color.set({ h: colors[0], s: colors[1], v: colors[2] });
      ignore_event = false;
      const h = Math.round(ColorPicker2.color.hsv.h);
      const s = Math.round(ColorPicker2.color.hsv.s);
      const v = Math.round(ColorPicker2.color.hsv.v);
      output.textContent = `${h}, ${s}, ${v}`;
      console.log("Border geändert")
    }
  )

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

window.change_border = change_border;
