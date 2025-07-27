# Dungeon Master's Tools
[![en](https://img.shields.io/badge/lang-en-green)](README.us.md)
---
[![ToDoList](https://img.shields.io/badge/Ir%20Para-To--Do%20List-blue)](ToDo-ptbr.md)

## Conceito
Esse projeto foi desenvolvido com intuíto de prover uma aplicação desktop, para uso em *D&D 4e e outros RPGs* por *Dungeon Masters*, que fosse de fácil manutenibilidade e expansível. Para tal o programa dispõe de uma funcionalidade básica para ler arquivos *sql* do antigo serviço *D&D Insiders* e mostrar esses dados em tabelas permitindo filtragem, busca e ordenação. Além, de dispor da capacidade de carregar *plugins* feitos por usuários.

## Pré-requisitos e recursos
O projeto utiliza Python 3.10.12, além de duas bibliotecas externas:
- PySide6, disponível em ([PyPi](https://pypi.org/project/PySide6/))
- yapsy, disponível em ([PyPi](https://pypi.org/project/Yapsy/))

## Passo a Passo
O projeto se deu da vontade de implementar uma alternativa ao software, baseado em java/javaFx, *Portable D&D Compendium* (infeliz indisponível para compartilhamento aqui). A processo de implementação se deu atráves de:
1. Baixar o software *Portable D&D Compendium*;
2. Extrair o conteudo do seu pacote javac;
3. Utilizar de ferramentas (vscode e JD-GUI) para descompilar o conteudo dos arquivos *class*;
4. Reproduzir parcialmente o funcionamento do seu *Parser* para os arquivos *SQL* do antigo *D&D Insider* (o resultado disso foi a classe [*DDIParser*](libs/DMTCore.py#L54));
5. A partir daqui o desenvolvimento focou-se em apresentar esses dados em um formato humano (uma tabela, parcialmente igual ao *Portable D&D Compendium*, o resultado é a classe [*CompendiumScreen*](libs/DMTCore.py#L1226));
6. Utilizando a documentação do [Pyside/QT](https://doc.qt.io/qtforpython-6/PySide6/QtWidgets/) e experimentação a recriação da tabela do software original foi alcançada com sucesso;
7. Fora a recriação do software original em Python/Pyside, buscou-se introduzir novas funcionalidades como a capacidade de carregar plugins e a criação de uma filtragem dinâmica baseada na categoria dos itens dispostos na tabela;
   1. ![JavaCompendium]()
   2. ![PythonCompendium]()
8. Como efeito colateral do uso de Python a aplicação agora é nativamente compátivel com linux e Windows e, possívelmente, qualquer sistema operacional que de suporte ao Python e a biblioteca Pyside6;

## Instalação
- Clone o projeto pelo git, ou faça o download pelo Github:
``` bash
git clone https://github.com/CMS999/Dungeon-Master-s-Tools.git
```
- ou
``` bash
git clone git@github.com:CMS999/Dungeon-Master-s-Tools.git
```

## Execução
- Na pasta raiz do projeto execute o arquivo main.py
``` bash
python main.py
```
- ou
``` bash
py main.py
```
## Bugs
Alguns bugs já são conhecidos, mas devido a natureza do projeto espera-se encontrar mais:
- O número no rodapé da página indicando a quantidade de itens sendo visualizados em um dado momento, ainda não está sendo atualizado sempre;
- A funcionalidade das *QToolBar* de cada aba, não funciona apropriadamente, abas sem um *QToolBar* associado geram uma *QToolbar* "fantasma";
- O programa não foi testado em nenhum momento em Windows e, embora, ele execute, é possível que diferenças de sistemas operacionais apareçam (Ex.: foi necessário adicionar um estilo 'Fusion' no app em *main.py*, pois o estilo padrão do Windows não estava sendo aplicado, como é no linux).

## Autor
- Cauã Marques da Silva ([GitHub](https://github.com/CMS999))

## Imagens