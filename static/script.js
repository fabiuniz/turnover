function extrairUrlsBasico(texto) {
    const regex = /(https?:\/\/[^\s]+)/g;
    const matches = texto.match(regex);
    return matches ? matches : [];
}

async function enviarDados(event) {
    event.preventDefault();
    const predictButton = document.getElementById("predictButton");
    const resultadoDiv = document.getElementById("resultado");

    // Show loading state
    predictButton.disabled = true;
    predictButton.innerHTML = 'Prever Turnover <span class="spinner"></span>';
    resultadoDiv.innerHTML = 'Previsão em andamento... <span class="spinner"></span>';

    const dados = {
        idade: parseInt(document.getElementById("idade").value),
        salario: parseFloat(document.getElementById("salario").value),
        tempo_empresa: parseInt(document.getElementById("tempo_empresa").value),
        avaliacao: parseFloat(document.getElementById("avaliacao").value)
    };

    try {
        const resposta = await fetch("http://vmlinuxd:8000/predict/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(dados)
        });

        if (!resposta.ok) {
            throw new Error(`Erro na API: ${resposta.status} - ${resposta.statusText}`);
        }

        const resultado = await resposta.json();
        resultadoDiv.innerHTML = `<strong>Chance de Turnover: ${resultado.chance_turnover}</strong>`;

    } catch (error) {
        resultadoDiv.innerHTML = `<span style="color: red;">Erro na previsão: ${error.message}</span>`;
        console.error("Erro ao enviar dados para a API:", error);
    } finally {
        // Reset button state
        predictButton.disabled = false;
        predictButton.innerHTML = 'Prever Turnover';
    }
}

async function abrirDashboard() {
    const dashboardBtn = document.querySelector('.dashboard-btn:nth-of-type(1)'); // Select the Dash button
    dashboardBtn.disabled = true;
    dashboardBtn.innerHTML = 'Iniciando Dash... <span class="spinner"></span>';

    const url = "http://vmlinuxd:8000/dashboard/";
    try {
        const resposta = await fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            }
        });

        if (!resposta.ok) {
            throw new Error(`Erro ao iniciar Dash: ${resposta.status} - ${resposta.statusText}`);
        }

        const resultado = await resposta.json();
        const message = resultado.message;
        const dashboardUrl = extrairUrlsBasico(message); // Extract URL from message

        if (dashboardUrl.length > 0) {
            if (confirm(message + "\n\nDeseja abrir o Dashboard agora?")) {
                window.open(dashboardUrl[0], '_blank');
            } else {
                alert("Dashboard (Dash) iniciado em segundo plano. Você pode acessá-lo mais tarde em " + dashboardUrl[0]);
            }
        } else {
            alert(message); // If no URL found in message
        }

    } catch (error) {
        alert(`Erro: ${error.message}`);
        console.error("Erro ao iniciar dashboard Dash:", error);
    } finally {
        dashboardBtn.disabled = false;
        dashboardBtn.innerHTML = 'Abrir Dashboard (Dash)';
    }
}

async function abrirStreamlit() {
    const streamlitBtn = document.querySelector('.dashboard-btn:nth-of-type(2)'); // Select the Streamlit button
    streamlitBtn.disabled = true;
    streamlitBtn.innerHTML = 'Iniciando Streamlit... <span class="spinner"></span>';

    const url = "http://vmlinuxd:8000/streamlit/";
    try {
        const resposta = await fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            }
        });

        if (!resposta.ok) {
            throw new Error(`Erro ao iniciar Streamlit: ${resposta.status} - ${resposta.statusText}`);
        }

        const resultado = await resposta.json();
        const message = resultado.message;
        const streamlitUrl = extrairUrlsBasico(message); // Extract URL from message

        if (streamlitUrl.length > 0) {
            if (confirm(message + "\n\nDeseja abrir o Dashboard agora?")) {
                window.open(streamlitUrl[0], '_blank');
            } else {
                alert("Dashboard (Streamlit) iniciado em segundo plano. Você pode acessá-lo mais tarde em " + streamlitUrl[0]);
            }
        } else {
            alert(message); // If no URL found in message
        }

    } catch (error) {
        alert(`Erro: ${error.message}`);
        console.error("Erro ao iniciar dashboard Streamlit:", error);
    } finally {
        streamlitBtn.disabled = false;
        streamlitBtn.innerHTML = 'Abrir Dashboard (Streamlit)';
    }
}

// Function to toggle the explanation box visibility
// Updated to accept an ID to toggle specific boxes
function toggleExplanation(boxId) {
    const explanationBox = document.getElementById(boxId);
    explanationBox.classList.toggle("show");
}