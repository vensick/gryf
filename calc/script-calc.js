
function recalc(changed) {
    const battle = parseFloat(document.getElementById("battle").value) || 0;
    const mode = parseFloat(document.getElementById("mode").value) || 1;
    const era = parseFloat(document.getElementById("era").value) || 1;
    const final = parseFloat(document.getElementById("final").value) || 0;

    const mult = mode * era;

    if (changed === "battle" || changed === "mode" || changed === "era") {
        document.getElementById("final").value = (battle * mult).toFixed(0);
    }

    if (changed === "final") {
        document.getElementById("battle").value = (final / mult).toFixed(0);
    }
}

document.getElementById("battle").oninput = () => recalc("battle");
document.getElementById("mode").oninput = () => recalc("mode");
document.getElementById("era").oninput = () => recalc("era");
document.getElementById("final").oninput = () => recalc("final");

function recalc(changed) {
    const battle = parseFloat(document.getElementById("battle").value) || 0;
    const mode = parseFloat(document.getElementById("mode").value) || 1;
    const era = parseFloat(document.getElementById("era").value) || 1;
    const final = parseFloat(document.getElementById("final").value) || 0;

    const mult = mode * era;

    if (changed === "battle" || changed === "mode" || changed === "era") {
        document.getElementById("final").value = (battle * mult).toFixed(0);
    }

    if (changed === "final") {
        document.getElementById("battle").value = (final / mult).toFixed(0);
    }
}

// przyciski trybów
const buttons = document.querySelectorAll(".type-buttons button");

buttons.forEach(btn => {
    btn.addEventListener("click", () => {
        buttons.forEach(b => b.classList.remove("active"));
        btn.classList.add("active");

        document.getElementById("mode").value = btn.dataset.mode;

        recalc("mode");
    });
});

// inputy
document.getElementById("battle").oninput = () => recalc("battle");
document.getElementById("mode").oninput = () => recalc("mode");
document.getElementById("era").oninput = () => recalc("era");
document.getElementById("final").oninput = () => recalc("final");
