const SALON_SMS = "+15192098803";

document.getElementById("y").textContent = new Date().getFullYear();

const form = document.getElementById("book-form");
const status = document.getElementById("status");
const dateInput = document.getElementById("date");

const tomorrow = new Date();
tomorrow.setDate(tomorrow.getDate() + 1);
dateInput.min = tomorrow.toISOString().slice(0, 10);

form.addEventListener("submit", (e) => {
  e.preventDefault();
  status.className = "form-status";
  status.textContent = "";

  if (!form.reportValidity()) {
    status.classList.add("err");
    status.textContent = "Fill the required fields.";
    return;
  }

  const data = Object.fromEntries(new FormData(form).entries());
  const lines = [
    "Kuzz Kreations booking request",
    `Name: ${data.name}`,
    `Phone: ${data.phone}`,
    data.email ? `Email: ${data.email}` : null,
    `Service: ${data.service}`,
    `Preferred: ${data.date} · ${data.time}`,
    data.notes ? `Notes: ${data.notes}` : null,
  ].filter(Boolean);

  const body = lines.join("\n");
  try {
    localStorage.setItem(
      "kuzz-booking-last",
      JSON.stringify({ ...data, at: new Date().toISOString() }),
    );
  } catch (_) {}

  const smsUrl = `sms:${SALON_SMS}?&body=${encodeURIComponent(body)}`;
  status.classList.add("ok");
  status.textContent = "Opening your messages app with the booking details…";
  window.location.href = smsUrl;

  setTimeout(() => {
    status.textContent =
      "If the text app didn’t open, call 519-209-8803 and read your preferred time.";
  }, 2500);
});
