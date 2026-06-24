async function sendMessage() {

    let input = document.getElementById("message");

    let message = input.value.trim();

    if (message === "") {
        return;
    }

    let chatBox = document.getElementById("chat-box");

    chatBox.innerHTML +=
        `<p><b>You:</b> ${message}</p>`;

    input.value = "";

    chatBox.innerHTML +=
        `<p id="loading"><b>Bot:</b> Thinking...</p>`;

    try {

        let response = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                message: message
            })
        });

        let data = await response.json();

        document.getElementById("loading").remove();

        chatBox.innerHTML +=
            `<p><b>Bot:</b> ${data.response}</p>`;

        chatBox.scrollTop =
            chatBox.scrollHeight;

    } catch (error) {

        document.getElementById("loading").remove();

        chatBox.innerHTML +=
            `<p><b>Bot:</b> Error connecting to server.</p>`;
    }
}


async function uploadPDF() {

    let fileInput =
        document.getElementById("pdfFile");

    if (fileInput.files.length === 0) {

        alert("Please select a PDF file.");

        return;
    }

    let file = fileInput.files[0];

    let formData = new FormData();

    formData.append("pdf", file);

    try {

        let response =
            await fetch("/upload", {
                method: "POST",
                body: formData
            });

        let data = await response.json();

        alert(data.message);

    } catch (error) {

        alert("Error uploading PDF.");
    }
}


document.addEventListener(
    "DOMContentLoaded",
    function () {

        let input =
            document.getElementById("message");

        input.addEventListener(
            "keypress",
            function (event) {

                if (event.key === "Enter") {

                    sendMessage();

                }

            }
        );
    }
);