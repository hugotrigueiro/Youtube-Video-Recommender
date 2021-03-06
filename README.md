# Recomendador de Vídeos do YouTube

Acesse a aplicação disponível com o [Recomendador de Vídeos do YouTube - by Hugo Trigueiro](https://ytvideo-recommender-by-hugo.herokuapp.com/)

<p align="center" style="margin-bottom: -10px">
    <img src="Demais Arquivos/git_demonstrativo.gif" alt="Gif Demonstrativo">
    <p align="center" style="font-size: 12px">Gif Demonstrativo</p>
</p>


## Sobre o projeto:
Este projeto foi baseado no projeto de execução ensinado no curso de [Como criar uma solução completa de Data Science | Mario Filho](http://mariofilho.com/curso/).

No curso, um recomendador de vídeos do YouTube é criado a partir de um processo End-to-End, ou seja, passando por todas as seguintes etapadas de desenvolvimento:
- Definição do Problema
- Coleta
- Limpeza
- Análise
- Modelagem
- Entrega dos resultados em uma solução adequada e acessível


## Ferramentas utilizadas:
Foram utilizadas as seguintes ferramentas na criação e execução do projeto:
- Linguagem de programação: Python
- IDE de desenvolvimento: Jupyter Lab
- Pacotes e Frameworks: 
    - gunicorn==20.0.4
    - Flask==1.0.0
    - requests==2.22.0
    - beautifulsoup4==4.8.0
    - pandas==0.25.1
    - numpy==1.16.2
    - matplotlib==2.1.2
    - scipy==1.3.1
    - scikit-learn==0.22.2.post1
    - lightgbm==2.3.1
    - joblib==0.14.1
- Linguagens e Frameworks usados no front-end:
    - HTML, CSS e JavaScript
    - Bootstrap
    - jQuery
- Ferramenta de conteinerização: Docker
- Plataforma de hospedagem em nuvem: Heroku
- Ferramentas auxiliares:
    - Anaconda, Visual Studio Code, Microsoft Excel, TextPad, Google Chrome

## Estrutura do Projeto:

### 1. Definição do Problema
A etapa inicial de qualquer projeto passa pela definição do problema que será resolvido. Então, por que criar um Recomendador de Vídeos do YouTube? Bom, nem sempre o YouTube recomenda vídeos que nós gostamos, correto? As vezes, na busca de vídeos com um conteúdo muito específico ou avançado de determinado tema, acabamos recebendo mais recomendações de vídeos muito populares ou de iniciantes, do que o conteúdo que de fato procuramos. Por exemplo, suponhamos que você goste muito de assistir vídeos sobre a aplicação de machine learning no campo da saúde. Devido as suas buscas, muito provavelmente o YouTube também irá te recomendar, por exemplo, vídeos genéricos sobre machine learning, inteligência artificial em carros autônomos, vídeo-aulas te ensinando a rodar o seu "primeiro modelo" e coisas do tipo. Portanto, foi definido uma estrutura simples para a definição do problema, como mostrado abaixo: 
- **Qual o problema a ser resolvido:** quero uma solução que entregue melhor os vídeos que eu busco.
- **O que irei fazer para resolver isso com Data Science:** criar um solução de recomendação de vídeos optimizada (um recomendador).
- **Como irei fazer:** criar uma solução com uma "linha de corte" de recomendação que me retorne um ranking de vídeos melhor recomendados
- **Como irei validar:**
    - Métrica primária: dos top N vídeos recomendados, quantos eu coloco na lista de Watch Later.
    - Métricas secundárias:
        - Quanto tempo eu passo selecionando vídeos para assistir no meu ranking.
        - Quantos vídeos eu de fato assisti por completo. 

É nesta etapa também que explicitamos algumas características do problema enfrentado. Portanto, para criar este Recomendador de Vídeos do YouTube, foi preciso identificar alguns pontos:
- Se trata de um problema de classificação
- Não há uma base de dados de partida, sendo preciso buscar estes dados diretamente do YouTube.
- Para realizar a busca de dados no YouTube, se faz necessário definir algumas palavras-chave de busca.
- Buscar dados da web podem demorar, assim é interessante controlar a quantidade de dados buscados e quanto tempo pode demorar este processo.
- A variável de predição (interesse nos vídeos) que será usada para treinar um modelo não é passível de ser coletada, então será necessário adicioná-la manualmente.
- Se tratando de um problema de classificação, podemos considerar o uso de modelos como: Decision Tree, Random Forest, LightGBM, Logistic Regression e SVM, por exemplo.

Com esse panorâma geral do problema definido, já se pode partir para as próximas etapas com uma melhor noção do que fazer no caminho a ser traçado.

### 2. Coleta dos Dados
A coleta dos dados se fez diretamente pela forma de Web Scraping, realizando a pesquisa com palavras-chave e "raspando" os dados da web da página do YouTube. Para realizar essa coleta é necessário algum conhecimento em HTML e CSS a fim de buscar e filtrar os dados procurados nas tags. Neste processo, também foi se escolhido um conjunto de campos a serem "raspados" das páginas de vídeos, nem todos são necessários para a modelagem, mas trazer muitas informações ajuda a enriquecer as possibilidades de análises posteriores.

### 3. Tratamento e Preparação dos Dados
Em geral, dados coletados através de Web Scraping costumam vir bastante "sujos", ou seja, dados em sua forma bruta que necessitam de camadas de limpeza e tratamento para que possam ser analisados. Nesta etapa, foram criadas algumas funções de extração de texto (usando expressões regulares), ajustes de datas e transformações numéricas que preparassem os dados para a análise. Durante esta etapa também foram criados os labels (variável y) de interesse nos vídeos de forma manual em uma planilha no Excel, este processo se deu com a leitura dos títulos e a classificação de **1 = Tenho interesse | 0 = Não tenho interesse.**

### 4. Análise dos Dados
Após a limpeza e preparação dos dados, o processo de análise acontece de forma mais fácil. Como o preenchimento dos labels de interesse foi feito manualmente a partir da leitura dos títulos dos vídeos, obviamente essa foi a primeira feature a ser selecionada para a modelagem. Para modelar os títulos também foi se utilizado o modelo TfidfVectorize do Scikit-Learn. Já considerando que o número de visualizações de um vídeo diz muito sobre a sua popularidade, uma feature com a média diária de views também foi gerada a partir da quantidade total de views de um vídeo desde a sua data de publicação. Outras análises também foram realizadas, mas considerando que o projeto tem uma característica de ser simples, apenas essas duas features foram usadas na modelagem até o momento.

### 5. Modelagem
Inicialmente nesta etapa, por não haver nenhuma solução já existente que pudesse servir de "base" ou "linha de corte" para as métricas de validação monitoradas nos modelos, um modelo simples de Árvore de Decisão (Decision Tree) foi criado para fazer este papel. Criada uma linha de corte, o restante da modelagem teve como foco melhorar as métricas acima desta linha. Foram testados mais dois modelos, Random Forest e LightGBM, além de um possível ensemble entre os mesmos. Contudo, tanto o Random Forest quanto o LightGBM apresentaram resultados semelhantes com o segundo tendo uma leve vantagem nas métricas avaliadas, sendo portanto escolhido como o modelo a ser usado.

### 6. Entrega dos Resultados
A entrega dos resultados previstos pelo modelo foi realizada através da criação e disponibilização de uma [aplicação online](https://ytvideo-recommender-by-hugo.herokuapp.com/) (feita em Flask) que realiza todo o processo de coleta, limpeza, preparação e predição dos dados. Também foi desenvolvida, para a entrega dos resultados, uma interface interativa com os top 5 vídeos com o melhor score de recomendação embedados diretamente em um objeto de carrossel interativo, além de também haver a opção de se abrir uma lista completa com os 30 vídeos melhor recomendados. A aplicação também está responsiva, podendo ser bem visualizada em dispositivos Mobile (Smartphones), Tablets e Desktop.

## Informações adicionais:
Autor - Hugo Trigueiro | Contatos: [Medium](https://medium.com/@hugotrigueiro) & [LinkedIn](https://www.linkedin.com/in/hugo-trigueiro/)

PS: Agradecimentos ao [Diego Zurita](https://github.com/DiegoZurita), tive um pequeno problema com o Docker e ele me deu uma força para resolver.