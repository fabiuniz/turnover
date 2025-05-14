        function extrairUrlsBasico(texto) {
          const regex = /(https?:\/\/[^\s]+)/g;
          const matches = texto.match(regex);
          return matches ? matches : [];
        }
        function msg(mensagem) {
          let url =extrairUrlsBasico(mensagem)
          const mensagemConfirmacao = mensagem + "\n";        
          if (confirm(mensagemConfirmacao)) {
            window.open(url, '_blank');
          } else {
            console.log("Abertura da URL cancelada pelo usuário.");
            // Você pode adicionar aqui alguma outra ação caso o usuário cancele.
          }
        }
        async function enviarDados(event) {
            event.preventDefault();
            const dados = {
                idade: parseInt(document.getElementById("idade").value),
                salario: parseFloat(document.getElementById("salario").value),
                tempo_empresa: parseInt(document.getElementById("tempo_empresa").value),
                avaliacao: parseFloat(document.getElementById("avaliacao").value)
            };
            const resposta = await fetch("http://vmlinuxd:8000/predict/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(dados)
            });
            const resultado = await resposta.json();
            document.getElementById("resultado").innerHTML = `Chance de Turnover: ${resultado.chance_turnover}`;
        }

        async function abrirDashboard() {
            const url= "http://vmlinuxd:8000/dashboard/";
            const resposta = await fetch(url, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                }
            });
            const resultado = await resposta.json();
            msg(resultado.message);
        }

        async function abrirStreamlit() {
            const url= "http://vmlinuxd:8000/streamlit/";
            const resposta = await fetch(url, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                }
            });
            const resultado = await resposta.json();
            msg(resultado.message);            
        }