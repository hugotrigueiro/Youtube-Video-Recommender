# Recomendador de vídeos do YouTube

Acesse a aplicação disponível com o [Recomendador de vídeos do YouTube - by Hugo Trigueiro](https://ytvideo-recommender-by-hugo.herokuapp.com/)


## Sobre o projeto:
Este projeto foi baseado no projeto de execução ensinado no [Curso de Data Science | Mario Filho](http://mariofilho.com/curso/).

O projeto consiste na criação de um recomendador de vídeos do YouTube a partir de um processo End-to-End, ou seja, passando por todas as seguintes etapadas de desenvolvimento:
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
    - Flask==0.12.2
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

### 1. Coleta de Dados
A coleta dos dados se fez diretamente pela forma de Web Scraping, realizando a pesquisa com palavras-chave e "raspando" os dados da web da página do YouTube. Para realizar essa coleta é necessário algum conhecimento em HTML e CSS a fim de buscar e filtrar os dados procurados nas tags de HTML corretamente.

### 2. Tratamento e Preparação dos Dados
Em geral, dados coletados através de Web Scraping costumam vir bastante "sujos", ou seja, dados em sua forma bruta que necessitam de camadas de limpeza e tratamento para que possam ser analisados. Nesta etapa, foram criadas algumas funções de extração de texto (usando expressões regulares), ajustes de datas e transformações numéricas que preparassem os dados para a análise. Durante esta etapa também foram criados os labels (variável y) de interesse nos vídeos de forma manual em uma planilha no Excel, este processo se deu com a leitura dos títutlos e a classificação de **1 = Interesse | 0 = Não Interesse.**

### 3. Análise dos Dados
Após a limpeza e preparação dos dados, o processo de análise acontece de forma mais fácil. Como o preenchimento dos labels de interesse nos vídeos feito manualmente a partir da leitura dos títulos, obviamente essa foi a primeira feature a ser selecionada para a modelagem. Para modelar os títulos dos vídeos, também foi utilizado o modelo TfidfVectorize do Scikit-Learn, Já considerando que o número de visualizações de um vídeo diz muito sobre a sua popularidade, uma feature de média de views diária também foi gerada a partir da quantidade total de views de um vídeo e da sua data de publicação. Outras análises também foram realizadas, mas considerando que o projeto tem uma característica de ser simples, apenas essas duas features foram usadas na modelagem.

### 4. Modelagem
Inicialmente nesta etapa, por não haver nenhuma solução já existente que servisse "base" ou "linha de corte" para as métricas de validação monitoradas nos modelos, um modelo simples de Árvore de Decisão (Decision Tree) foi criado para fazer este papel. Criada uma linha de corte, o restante da modelagem teve como foco melhorar as métricas acima desta linha. Foram testados mais dois modelos, Random Forest e LightGBM, além de um possível ensemble entre os mesmos. Contudo, tanto o Random Forest quanto o LightGBM apresentaram resultados semelhantes com o segundo tendo uma leve vantagem nas métricas de avaliação, sendo portanto escolhido como o modelo a ser usado.

### 5. Entrega dos Resultados
A entrega dos resultados previstos pelo modelo foi realizada através da criação e disponibilização de uma [aplicação online](https://ytvideo-recommender-by-hugo.herokuapp.com/) (feita em Flask) que realiza todo o processo de coleta, limpeza, preparação e predição dos dados. Também foi desenvolvida, para a entrega dos resultados, uma interface interativa com os top 5 vídeos com o melhor score de recomendação embedados diretamente em um objeto de carrossel interativo além de também haver a opção de se abrir uma lista completa com os 30 vídeos melhor recomendados. A aplicação também está responsiva, podendo ser bem visualizada em dispositivos Mobile (Smartphones), Tablets e Desktop. 