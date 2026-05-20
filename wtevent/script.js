/* ============================
    TOGGLE – POKAŻ/UKRYJ USTAWIENIA
   ============================ */

const storageKey = "wteventInputsCollapsed";
const toggleBtn = document.getElementById("toggleInputs");
const inputsGroup = document.getElementById("inputsGroup");

function setInputsCollapsed(collapsed) {
  if (collapsed) {
    inputsGroup.classList.add("collapsed");
    toggleBtn.textContent = "Ustawienia (rozwiń)";
  } else {
    inputsGroup.classList.remove("collapsed");
    toggleBtn.textContent = "Ustawienia (zwiń)";
  }
  localStorage.setItem(storageKey, collapsed ? "1" : "0");
}

toggleBtn.addEventListener("click", () => {
  const collapsed = !inputsGroup.classList.contains("collapsed");
  setInputsCollapsed(collapsed);
});

// Po załadowaniu strony przywróć stan
const saved = localStorage.getItem(storageKey);
setInputsCollapsed(saved === "1");

/* ============================
   LOCAL STORAGE – ZAPIS/ODCZYT
   ============================ */

const fields = ["event-date", "event-time", "stages", "upgrade-points"];

function saveSettings() {
  fields.forEach(id => {
    const el = document.getElementById(id);
    localStorage.setItem(id, el.value);
  });
}

function loadSettings() {
  fields.forEach(id => {
    const saved = localStorage.getItem(id);
    if (saved !== null) {
      document.getElementById(id).value = saved;
    }
  });
}

/* ============================
   GŁÓWNY PANEL
   ============================ */

function updatePanel() {
  const date = document.getElementById('event-date').value;
  const time = document.getElementById('event-time').value;
  const stages = Number(document.getElementById('stages').value);
  const upgrade = Number(document.getElementById('upgrade-points').value);
  const out = document.getElementById('output');

  if (!date || !time || !stages || !upgrade) {
    out.textContent = "Uzupełnij wszystkie pola.";
    return;
  }

  const start = new Date(date + "T" + time);
  const now = new Date();

  const eventDurationMs = stages * 2 * 24 * 60 * 60 * 1000;
  const end = new Date(start.getTime() + eventDurationMs);

  if (now < start) {
    out.textContent = "Event jeszcze się nie zaczął.";
    return;
  }

  if (now > end) {
    out.textContent = "Event już się skończył.";
    return;
  }

  const remainingMs = end - now;
  const remainingDays = (remainingMs / (1000 * 60 * 60 * 24)).toFixed(2);

  const msSinceStart = now - start;
  const stageLengthMs = 2 * 24 * 60 * 60 * 1000;
  const currentStage = Math.floor(msSinceStart / stageLengthMs) + 1;

  const stageEnd = new Date(start.getTime() + currentStage * stageLengthMs);
  const stageRemainingMs = stageEnd - now;
  const stageRemainingHours = (stageRemainingMs / (1000 * 60 * 60)).toFixed(1);

  // PUNKTY DZIENNIE Z CAŁEGO EVENTU
  const totalDays = stages * 2;
  const pointsPerDay = upgrade / totalDays;

  out.innerHTML = `
    <b>Aktualny etap:</b> ${currentStage} / ${stages}<br>
    <b>Czas do końca etapu:</b> ${stageRemainingHours} h<br>
    <b>Czas do końca eventu:</b> ${remainingDays} dni<br>
    <b>Punkty do zrobienia dziennie:</b> ${Math.ceil(pointsPerDay).toLocaleString('pl-PL')}
  `;
}

/* ============================
   LICZNIK "POWINIENEŚ MIEĆ TERAZ"
   ============================ */

function updateRequiredPoints() {
  const date = document.getElementById('event-date').value;
  const time = document.getElementById('event-time').value;
  const stages = Number(document.getElementById('stages').value);
  const upgrade = Number(document.getElementById('upgrade-points').value);

  if (!date || !time || !stages || !upgrade) return;

  const start = new Date(date + "T" + time);
  const now = new Date();

  const eventDurationMs = stages * 2 * 24 * 60 * 60 * 1000;
  const end = new Date(start.getTime() + eventDurationMs);

  if (now < start || now > end) return;

  const totalSeconds = (end - start) / 1000;
  const elapsedSeconds = (now - start) / 1000;

  const progress = elapsedSeconds / totalSeconds;
  const requiredPointsNow = Math.floor(progress * upgrade);

  document.getElementById("required-now").textContent =
    requiredPointsNow.toLocaleString("pl-PL");
}

function resetAll() {
  localStorage.clear();
  document.getElementById('event-date').value = "";
  document.getElementById('event-time').value = "";
  document.getElementById('stages').value = "";
  document.getElementById('upgrade-points').value = "";
  updatePanel();
  updateRequiredPoints();
}


/* ============================
   START
   ============================ */

loadSettings();
updatePanel();
updateRequiredPoints();

document.querySelectorAll("input").forEach(el => {
  el.addEventListener("input", () => {
    saveSettings();
    updatePanel();
  });
});

setInterval(() => {
  updatePanel();
  updateRequiredPoints();
}, 1000);
