document.addEventListener("DOMContentLoaded", function() {
    const canvas = document.getElementById("wheelCanvas");
    const ctx = canvas.getContext("2d");
    const resultText = document.getElementById("result");
    const jobcardButton = document.getElementById("jobcardButton"); // Show details button

    let spinning = false;
    let spinSpeed = 0;
    let startAngle = 0;
    let selectedJob = "";
    const numSegments = jobs.length;
    const anglePerSegment = (2 * Math.PI) / numSegments;
    const centerX = canvas.width / 2;
    const centerY = canvas.height / 2;
    const radius = 180;

    // Define colors dynamically
    const colors = ["#FF5733", "#33FF57", "#3357FF", "#FF33A1", "#F3FF33", "#FFA500", "#800080", "#00CED1", "#FFD700"];

    function drawWheel() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        for (let i = 0; i < numSegments; i++) {
            let start = startAngle + i * anglePerSegment;
            let end = startAngle + (i + 1) * anglePerSegment;

            ctx.beginPath();
            ctx.moveTo(centerX, centerY);
            ctx.arc(centerX, centerY, radius, start, end);
            ctx.fillStyle = colors[i % colors.length];
            ctx.fill();
            ctx.stroke();
            ctx.closePath();

            // Draw text
            ctx.save();
            ctx.translate(centerX, centerY);
            ctx.rotate(start + anglePerSegment / 2);
            ctx.fillStyle = "#000";
            ctx.font = "16px Arial";
            ctx.textAlign = "center";
            ctx.fillText(jobs[i], radius - 30, 5);
            ctx.restore();
        }

        // Draw arrow (indicator)
        ctx.beginPath();
        ctx.moveTo(centerX - 10, centerY - radius - 10);
        ctx.lineTo(centerX + 10, centerY - radius - 10);
        ctx.lineTo(centerX, centerY - radius);
        ctx.fillStyle = "red";
        ctx.fill();
    }

    function spinWheel() {
        if (spinning) return;
        spinning = true;
        spinSpeed = Math.random() * 20 + 10;

        function animateSpin() {
            if (spinSpeed > 0.2) {
                startAngle += (spinSpeed * Math.PI) / 180;
                spinSpeed *= 0.98;
                requestAnimationFrame(animateSpin);
            } else {
                spinning = false;
                selectJob();
            }
            drawWheel();
        }

        animateSpin();
    }

    function selectJob() {
        const pointerAngle = (3 * Math.PI) / 2; // Indicator at top
        let normalizedStartAngle = startAngle % (2 * Math.PI);
        if (normalizedStartAngle < 0) normalizedStartAngle += 2 * Math.PI;
        let adjustedAngle = pointerAngle - normalizedStartAngle;
        if (adjustedAngle < 0) adjustedAngle += 2 * Math.PI;
        const segmentAngle = (2 * Math.PI) / numSegments;
        let selectedIndex = Math.floor(adjustedAngle / segmentAngle);
        selectedJob = jobs[selectedIndex];

        resultText.innerText = "Selected: " + selectedJob;
        jobcardButton.style.display = "block"; // Show button

        // Send the selected job to Flask
        fetch("/set_selected_job", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ job: selectedJob })
        }).then(response => response.json());

        canvas.removeEventListener("click", spinWheel); // Disable further spins
    }

    jobcardButton.addEventListener("click", function() {
        window.location.href = "/jobcard"; // Redirect to job details
    });

    canvas.addEventListener("click", spinWheel);
    drawWheel();
});
