# documentação de código
Este código é um serviço web implementado em Flask que calcula o intervalo entre vitórias consecutivas de um cineasta. Leia um arquivo CSV contendo informações do filme, identifique as editoras vencedoras e calcule os intervalos máximo e mínimo entre as vitórias de cada editora.

### Bibliotecas usadas
- "Flask": estrutura web Python. - Pandas: Para processamento de dados. - "jsonify": Formate a saída no formato JSON. 

### Função principal
- "calcular_intervalos(df)": Função que calcula o intervalo entre vitórias sucessivas do produtor. - "show_intervals()": Caminho que calcula os intervalos utilizando a função "calcular_intervalos()" e os retorna no formato JSON.

### Fluxo de implementação
1. Carregue dados de um arquivo CSV. dois. Identificação do fabricante vencedor. 3. Calcule o intervalo entre vitórias de cada produtor. 4. Gere JSON contendo os maiores e menores intervalos de cada fabricante. 5. Retorna JSON com resultados.

## Rota
- "/outputFinal": Rota padrão que retorna o intervalo máximo e mínimo entre vitórias do produtor.

## Implementação
A execução do código iniciará o servidor Flask localmente. Você pode visualizar os resultados do cálculo acessando o caminho `/outputFinal. Substitua o caminho do arquivo CSV pelo local correto do arquivo de dados.