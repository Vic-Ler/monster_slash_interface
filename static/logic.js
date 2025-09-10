async function submitPlayerForm(event) {
  event.preventDefault();

  const data = {
    player: document.getElementById("playerName").value,
    weapon: document.getElementById("weapon").value,
    monster: document.getElementById("monster").value,
    hp: document.getElementById("hp").value
  };

  const res = await fetch("/api/submit", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data)
  });

  const result = await res.json();
  document.getElementById("status").innerText = 
    "Gesendet! Runde " + result.round;
}

async function loadRoundData() {
  const round = document.getElementById("currentRound").innerText;
  const res = await fetch("/api/round/" + round);
  const players = await res.json();

  const list = document.getElementById("playerList");
  list.innerHTML = "";
  players.forEach(p => {
    const li = document.createElement("li");
    li.innerText = `${p.player} | Waffe: ${p.weapon} | Monster: ${p.monster} | HP: ${p.hp}`;
    list.appendChild(li);
  });
}

async function closeRound() {
  const res = await fetch("/api/close_round", { method: "POST" });
  const result = await res.json();
  document.getElementById("currentRound").innerText = result.new_round;
  document.getElementById("playerList").innerHTML = "";
}

document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("playerForm");
  if (form) {
    form.addEventListener("submit", submitPlayerForm);
  }
});
